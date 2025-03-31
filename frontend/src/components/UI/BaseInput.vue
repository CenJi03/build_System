<template>
  <div class="base-input">
    <label v-if="label" :for="id" class="base-input-label">{{ label }}</label>
    <div class="input-container" :class="{ 'has-error': error }">
      <input
        :id="id"
        :type="type"
        :value="modelValue"
        :disabled="disabled"
        :placeholder="placeholder"
        @input="updateValue($event)"
        class="base-input-field"
      />
    </div>
    <span v-if="error" class="base-input-error">{{ error }}</span>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue'

const props = defineProps({
  id: {
    type: String,
    required: true
  },
  label: {
    type: String,
    default: ''
  },
  modelValue: {
    type: [String, Number],
    default: ''
  },
  type: {
    type: String,
    default: 'text'
  },
  error: {
    type: String,
    default: ''
  },
  disabled: {
    type: Boolean,
    default: false
  },
  placeholder: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['update:modelValue'])

function updateValue(event) {
  emit('update:modelValue', event.target.value)
}
</script>

<style scoped>
.base-input {
  margin-bottom: 1rem;
}

.base-input-label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: #333;
}

.input-container {
  position: relative;
}

.base-input-field {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  transition: border-color 0.2s ease;
}

.base-input-field:focus {
  outline: none;
  border-color: #4a90e2;
  box-shadow: 0 0 0 2px rgba(74, 144, 226, 0.2);
}

.base-input-field:disabled {
  background-color: #f5f5f5;
  cursor: not-allowed;
}

.has-error .base-input-field {
  border-color: #dc3545;
}

.base-input-error {
  display: block;
  color: #dc3545;
  font-size: 0.8rem;
  margin-top: 0.25rem;
}
</style>