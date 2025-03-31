<template>
    <button 
      :type="type" 
      :disabled="disabled"
      :class="[
        'base-button', 
        `base-button--${variant}`,
        { 'base-button--disabled': disabled }
      ]"
      @click="$emit('click')"
    >
      <slot>{{ text }}</slot>
    </button>
  </template>
  
  <script setup>
  defineProps({
    type: {
      type: String,
      default: 'button',
      validator: (value) => ['button', 'submit', 'reset'].includes(value)
    },
    text: {
      type: String,
      default: ''
    },
    disabled: {
      type: Boolean,
      default: false
    },
    variant: {
      type: String,
      default: 'primary',
      validator: (value) => ['primary', 'secondary', 'danger', 'success'].includes(value)
    }
  })
  
  defineEmits(['click'])
  </script>
  
  <style scoped>
  .base-button {
    padding: 10px 15px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-weight: bold;
    transition: background-color 0.3s ease, opacity 0.3s ease;
  }
  
  .base-button--primary {
    background-color: #007bff;
    color: white;
  }
  
  .base-button--secondary {
    background-color: #6c757d;
    color: white;
  }
  
  .base-button--danger {
    background-color: #dc3545;
    color: white;
  }
  
  .base-button--success {
    background-color: #28a745;
    color: white;
  }
  
  .base-button--disabled {
    background-color: #cccccc;
    cursor: not-allowed;
    opacity: 0.65;
  }
  
  .base-button:hover:not(.base-button--disabled) {
    opacity: 0.9;
  }
  </style>