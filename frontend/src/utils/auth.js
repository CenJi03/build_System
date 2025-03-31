/**
 * Auth utility functions
 */

/**
 * Parses and returns the payload of a JWT token
 * @param {string} token - JWT token
 * @returns {object|null} Decoded token payload or null if invalid
 */
export function parseJwt(token) {
  try {
    const base64Url = token.split('.')[1];
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    const jsonPayload = decodeURIComponent(
      atob(base64)
        .split('')
        .map(c => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
        .join('')
    );
    return JSON.parse(jsonPayload);
  } catch (error) {
    return null;
  }
}

/**
 * Checks if a token is expired
 * @param {string} token - JWT token
 * @returns {boolean} True if token is expired or invalid, false otherwise
 */
export function isTokenExpired(token) {
  const payload = parseJwt(token);
  if (!payload || !payload.exp) return true;
  
  const expiryDate = new Date(payload.exp * 1000);
  const currentDate = new Date();
  
  return currentDate >= expiryDate;
}

/**
 * Gets token expiration date
 * @param {string} token - JWT token
 * @returns {Date|null} Expiration date or null if invalid
 */
export function getTokenExpiryDate(token) {
  const payload = parseJwt(token);
  if (!payload || !payload.exp) return null;
  
  return new Date(payload.exp * 1000);
}
