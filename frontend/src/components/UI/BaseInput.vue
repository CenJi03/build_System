<template>
  <div class="base-input">
    <label v-if="label" :for="id">{{ label }}</label>
    <div class="input-wrapper">
      <input
        :id="id"
        :type="showPassword ? 'text' : type"
        :value="modelValue"
        @input="$emit('update:modelValue', $event.target.value)"
        :placeholder="placeholder"
        :required="required"
        :disabled="disabled"
        :class="{ 'input-error': error }"
      />
      <button 
        v-if="type === 'password'" 
        type="button" 
        class="password-toggle" 
        @mousedown="showPasswordStart"
        @mouseup="showPasswordEnd"
        @mouseleave="showPasswordEnd"
        @touchstart="showPasswordStart"
        @touchend="showPasswordEnd"
        @touchcancel="showPasswordEnd"
        :aria-label="showPassword ? 'Release to hide password' : 'Hold to show password'"
      >
        <svg 
          class="eye-icon" 
          xmlns="http://www.w3.org/2000/svg" 
          width="16" 
          height="16" 
          viewBox="0 0 24 24" 
          fill="none" 
          stroke="currentColor" 
          stroke-width="2" 
          stroke-linecap="round" 
          stroke-linejoin="round"
        >
          <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
          <circle cx="12" cy="12" r="3"></circle>
        </svg>
      </button>
    </div>
    <span v-if="error" class="error-message">{{ error }}</span>
  </div>
</template>

<script setup>
import { ref } from 'vue';

defineProps({
  id: {
    type: String,
    required: true
  },
  label: {
    type: String,
    default: ''
  },
  type: {
    type: String,
    default: 'text'
  },
  modelValue: {
    type: [String, Number],
    default: ''
  },
  placeholder: {
    type: String,
    default: ''
  },
  required: {
    type: Boolean,
    default: false
  },
  disabled: {
    type: Boolean,
    default: false
  },
  error: {
    type: String,
    default: ''
  }
});

defineEmits(['update:modelValue']);

const showPassword = ref(false);

// Show password while button is pressed
function showPasswordStart() {
  showPassword.value = true;
}

// Hide password when button is released
function showPasswordEnd() {
  showPassword.value = false;
}
</script>

<style scoped>
.base-input {
  margin-bottom: 15px;
}

label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

input {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  transition: border-color 0.3s ease;
}

input:focus {
  outline: none;
  border-color: #007bff;
}

.input-error {
  border-color: red;
}

.error-message {
  color: red;
  font-size: 0.8em;
  margin-top: 5px;
}

input:disabled {
  background-color: #f4f4f4;
  cursor: not-allowed;
}

.password-toggle {
  position: absolute;
  right: 8px;
  background: none;
  border: none;
  cursor: pointer;
  color: #606060;
  padding: 4px;
  border-radius: 3px;
  background-color: #f1f1f1;
  transition: background-color 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.password-toggle:active {
  background-color: #e0e0e0;
}

.eye-icon {
  pointer-events: none;
}
</style>