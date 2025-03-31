export const validators = {
  required: (value) => !!value || 'This field is required',
  
  email: (value) => {
    const pattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    return pattern.test(value) || 'Must be a valid email'
  },
  
  minLength: (min) => (value) => 
    (value && value.length >= min) || `Must be at least ${min} characters`,
  
  maxLength: (max) => (value) => 
    (value && value.length <= max) || `Must be no more than ${max} characters`,
  
  passwordStrength: (value) => {
    const hasUpperCase = /[A-Z]/.test(value)
    const hasLowerCase = /[a-z]/.test(value)
    const hasNumber = /[0-9]/.test(value)
    const hasSpecialChar = /[!@#$%^&*(),.?":{}|<>]/.test(value)
    
    return (
      (hasUpperCase && hasLowerCase && hasNumber && hasSpecialChar && value.length >= 8) ||
      'Password must be at least 8 characters with uppercase, lowercase, number, and special character'
    )
  },
  
  passwordMatch: (confirmValue) => (value) => 
    value === confirmValue || 'Passwords do not match'
}

export function validate(value, ...rules) {
  for (const rule of rules) {
    const result = rule(value)
    if (result !== true) return result
  }
  return true
}