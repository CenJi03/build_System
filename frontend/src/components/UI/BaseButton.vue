<template>
  <button
    :type="type"
    :class="['base-button', `variant-${variant}`, { 'full-width': fullWidth }]"
    :disabled="disabled"
    @click="$emit('click', $event)"
  >
    <slot></slot>
  </button>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue'

defineProps({
  type: {
    type: String,
    default: 'button'
  },
  variant: {
    type: String,
    default: 'primary',
    validator: (value) => ['primary', 'secondary', 'danger', 'success', 'warning', 'text'].includes(value)
  },
  disabled: {
    type: Boolean,
    default: false
  },
  fullWidth: {
    type: Boolean,
    default: false
  }
})

defineEmits(['click'])
</script>

<style scoped>
.base-button {
  padding: 0.75rem 1.5rem;
  border-radius: 4px;
  font-weight: 600;
  border: none;
  cursor: pointer;
  transition: background-color 0.2s ease, transform 0.1s ease;
  font-size: 1rem;
}

.base-button:hover:not(:disabled) {
  opacity: 0.9;
}

.base-button:active:not(:disabled) {
  transform: translateY(1px);
}

.base-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.variant-primary {
  background-color: #007bff;
  color: white;
}

.variant-secondary {
  background-color: #6c757d;
  color: white;
}

.variant-danger {
  background-color: #dc3545;
  color: white;
}

.variant-success {
  background-color: #28a745;
  color: white;
}

.variant-warning {
  background-color: #ffc107;
  color: #212529;
}

.variant-text {
  background-color: transparent;
  color: #007bff;
  padding: 0.5rem;
}

.full-width {
  width: 100%;
}
</style>