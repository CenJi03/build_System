-- Create Extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Enum for User Roles
CREATE TYPE user_role AS ENUM ('admin', 'user', 'manager', 'support');

-- Enum for Account Status
CREATE TYPE account_status AS ENUM ('active', 'suspended', 'pending_verification', 'locked');

-- Users Table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    role user_role DEFAULT 'user',
    status account_status DEFAULT 'pending_verification',
    
    -- Authentication Tracking
    last_login TIMESTAMP,
    date_joined TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_password_change TIMESTAMP,
    
    -- Security Features
    is_verified BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    failed_login_attempts INTEGER DEFAULT 0,
    lockout_timestamp TIMESTAMP,
    
    -- Two-Factor Authentication
    two_factor_secret VARCHAR(255),
    two_factor_enabled BOOLEAN DEFAULT FALSE,
    
    -- Audit Fields
    created_by UUID,
    updated_by UUID,
    
    CONSTRAINT fk_created_by FOREIGN KEY (created_by) REFERENCES users(id),
    CONSTRAINT fk_updated_by FOREIGN KEY (updated_by) REFERENCES users(id)
);

-- Password History Table (for preventing password reuse)
CREATE TABLE password_history (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Login Attempt Logs
CREATE TABLE login_attempts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID,
    ip_address INET NOT NULL,
    attempt_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_successful BOOLEAN DEFAULT FALSE,
    user_agent TEXT,
    
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Email Verification Tokens
CREATE TABLE email_verification_tokens (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL,
    token VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL,
    is_used BOOLEAN DEFAULT FALSE,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Password Reset Tokens
CREATE TABLE password_reset_tokens (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL,
    token VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL,
    is_used BOOLEAN DEFAULT FALSE,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Audit Log Table
CREATE TABLE user_activity_log (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL,
    action_type VARCHAR(50) NOT NULL, -- login, logout, profile_update, password_change
    ip_address INET,
    user_agent TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    details JSONB,
    
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- User Sessions Table
CREATE TABLE user_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL,
    session_token VARCHAR(255) NOT NULL,
    ip_address INET,
    user_agent TEXT,
    device_info JSONB,
    login_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expiry_timestamp TIMESTAMP NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    logout_timestamp TIMESTAMP,
    logout_reason VARCHAR(50), -- 'user_logout', 'session_expired', 'admin_termination', 'security_violation'
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Indexes for Performance
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_login_attempts_user ON login_attempts(user_id);
CREATE INDEX idx_login_attempts_timestamp ON login_attempts(attempt_timestamp);
CREATE INDEX idx_activity_log_user ON user_activity_log(user_id);
CREATE INDEX idx_activity_log_timestamp ON user_activity_log(timestamp);

-- Indexes for Session Management
CREATE INDEX idx_user_sessions_user_id ON user_sessions(user_id);
CREATE INDEX idx_user_sessions_token ON user_sessions(session_token);
CREATE INDEX idx_user_sessions_is_active ON user_sessions(is_active);
CREATE INDEX idx_user_sessions_expiry ON user_sessions(expiry_timestamp) WHERE is_active = TRUE;

-- Function to log user activities
CREATE OR REPLACE FUNCTION log_user_activity(
    p_user_id UUID, 
    p_action_type VARCHAR(50), 
    p_ip_address INET DEFAULT NULL, 
    p_user_agent TEXT DEFAULT NULL, 
    p_details JSONB DEFAULT NULL
) RETURNS VOID AS $$
BEGIN
    INSERT INTO user_activity_log (
        user_id, 
        action_type, 
        ip_address, 
        user_agent, 
        details
    ) VALUES (
        p_user_id, 
        p_action_type, 
        p_ip_address, 
        p_user_agent, 
        p_details
    );
END;
$$ LANGUAGE plpgsql;

-- Function to check and update login attempts
CREATE OR REPLACE FUNCTION update_login_attempts(
    p_user_id UUID, 
    p_is_successful BOOLEAN, 
    p_ip_address INET, 
    p_user_agent TEXT
) RETURNS VOID AS $$
DECLARE
    max_attempts INTEGER := 5;
    current_attempts INTEGER;
BEGIN
    -- Log the login attempt
    INSERT INTO login_attempts (
        user_id, 
        ip_address, 
        is_successful,
        user_agent
    ) VALUES (
        p_user_id, 
        p_ip_address, 
        p_is_successful,
        p_user_agent
    );

    -- If login failed, increment failed attempts
    IF NOT p_is_successful THEN
        UPDATE users 
        SET failed_login_attempts = failed_login_attempts + 1,
            lockout_timestamp = CASE 
                WHEN failed_login_attempts + 1 >= max_attempts 
                THEN CURRENT_TIMESTAMP + INTERVAL '15 minutes'
                ELSE lockout_timestamp 
            END
        WHERE id = p_user_id;
    ELSE
        -- Reset failed attempts on successful login
        UPDATE users 
        SET failed_login_attempts = 0,
            lockout_timestamp = NULL,
            last_login = CURRENT_TIMESTAMP
        WHERE id = p_user_id;
    END IF;
END;
$$ LANGUAGE plpgsql;

-- Function to create a new user session
CREATE OR REPLACE FUNCTION create_user_session(
    p_user_id UUID,
    p_session_token VARCHAR(255),
    p_ip_address INET,
    p_user_agent TEXT,
    p_device_info JSONB DEFAULT NULL,
    p_session_duration INTERVAL DEFAULT INTERVAL '24 hours'
) RETURNS UUID AS $$
DECLARE
    session_id UUID;
BEGIN
    INSERT INTO user_sessions (
        user_id,
        session_token,
        ip_address,
        user_agent,
        device_info,
        expiry_timestamp
    ) VALUES (
        p_user_id,
        p_session_token,
        p_ip_address,
        p_user_agent,
        p_device_info,
        CURRENT_TIMESTAMP + p_session_duration
    ) RETURNING id INTO session_id;
    
    -- Log the login activity
    PERFORM log_user_activity(
        p_user_id, 
        'login', 
        p_ip_address, 
        p_user_agent, 
        jsonb_build_object('session_id', session_id)
    );
    
    RETURN session_id;
END;
$$ LANGUAGE plpgsql;

-- Function to end a user session (logout)
CREATE OR REPLACE FUNCTION end_user_session(
    p_session_token VARCHAR(255),
    p_logout_reason VARCHAR(50) DEFAULT 'user_logout'
) RETURNS BOOLEAN AS $$
DECLARE
    v_user_id UUID;
    v_ip_address INET;
    v_user_agent TEXT;
    v_session_exists BOOLEAN;
BEGIN
    -- Get session info and mark it as inactive
    UPDATE user_sessions 
    SET is_active = FALSE,
        logout_timestamp = CURRENT_TIMESTAMP,
        logout_reason = p_logout_reason
    WHERE session_token = p_session_token
      AND is_active = TRUE
    RETURNING user_id, ip_address, user_agent, TRUE INTO v_user_id, v_ip_address, v_user_agent, v_session_exists;
    
    -- If session exists, log the logout activity
    IF v_session_exists THEN
        PERFORM log_user_activity(
            v_user_id, 
            'logout', 
            v_ip_address, 
            v_user_agent, 
            jsonb_build_object('reason', p_logout_reason)
        );
        RETURN TRUE;
    ELSE
        RETURN FALSE;
    END IF;
END;
$$ LANGUAGE plpgsql;

-- Function to terminate all sessions for a user (force logout from all devices)
CREATE OR REPLACE FUNCTION terminate_all_user_sessions(
    p_user_id UUID,
    p_logout_reason VARCHAR(50) DEFAULT 'admin_termination'
) RETURNS INTEGER AS $$
DECLARE
    terminated_count INTEGER;
BEGIN
    UPDATE user_sessions 
    SET is_active = FALSE,
        logout_timestamp = CURRENT_TIMESTAMP,
        logout_reason = p_logout_reason
    WHERE user_id = p_user_id
      AND is_active = TRUE;
    
    GET DIAGNOSTICS terminated_count = ROW_COUNT;
    
    -- Log the mass termination if any sessions were terminated
    IF terminated_count > 0 THEN
        PERFORM log_user_activity(
            p_user_id, 
            'sessions_terminated', 
            NULL, 
            NULL, 
            jsonb_build_object('count', terminated_count, 'reason', p_logout_reason)
        );
    END IF;
    
    RETURN terminated_count;
END;
$$ LANGUAGE plpgsql;

-- Function to update session activity timestamp
CREATE OR REPLACE FUNCTION update_session_activity(
    p_session_token VARCHAR(255)
) RETURNS BOOLEAN AS $$
DECLARE
    session_updated BOOLEAN;
BEGIN
    UPDATE user_sessions 
    SET last_activity = CURRENT_TIMESTAMP
    WHERE session_token = p_session_token
      AND is_active = TRUE
    RETURNING TRUE INTO session_updated;
    
    RETURN COALESCE(session_updated, FALSE);
END;
$$ LANGUAGE plpgsql;

-- View for active sessions
CREATE OR REPLACE VIEW active_sessions AS
SELECT 
    s.id AS session_id,
    u.username,
    u.email,
    s.ip_address,
    s.user_agent,
    s.login_timestamp,
    s.last_activity,
    s.expiry_timestamp,
    EXTRACT(EPOCH FROM (s.expiry_timestamp - CURRENT_TIMESTAMP)) AS seconds_until_expiry
FROM 
    user_sessions s
JOIN 
    users u ON s.user_id = u.id
WHERE 
    s.is_active = TRUE
    AND s.expiry_timestamp > CURRENT_TIMESTAMP;

-- Automatically clean up expired sessions
CREATE OR REPLACE FUNCTION cleanup_expired_sessions() RETURNS INTEGER AS $$
DECLARE
    expired_count INTEGER;
BEGIN
    UPDATE user_sessions 
    SET is_active = FALSE,
        logout_timestamp = CURRENT_TIMESTAMP,
        logout_reason = 'session_expired'
    WHERE is_active = TRUE
      AND expiry_timestamp < CURRENT_TIMESTAMP;
    
    GET DIAGNOSTICS expired_count = ROW_COUNT;
    RETURN expired_count;
END;
$$ LANGUAGE plpgsql;

-- Comments for documentation
COMMENT ON TABLE users IS 'Stores user account information with enhanced security features';
COMMENT ON TABLE login_attempts IS 'Tracks all login attempts for security monitoring';
COMMENT ON TABLE user_activity_log IS 'Comprehensive log of user activities for auditing';
COMMENT ON TABLE user_sessions IS 'Tracks active user sessions and logout events';
COMMENT ON FUNCTION create_user_session IS 'Creates a new session when user logs in';
COMMENT ON FUNCTION end_user_session IS 'Ends a session when user logs out';
COMMENT ON FUNCTION terminate_all_user_sessions IS 'Terminates all active sessions for a user';
COMMENT ON VIEW active_sessions IS 'Lists all currently active user sessions';