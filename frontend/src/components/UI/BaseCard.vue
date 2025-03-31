<template>
  <div class="base-card" :class="{ 'with-shadow': shadow }">
    <div v-if="title || $slots.header" class="card-header">
      <slot name="header">
        <h3>{{ title }}</h3>
      </slot>
    </div>
    
    <div class="card-body">
      <slot></slot>
    </div>
    
    <div v-if="$slots.footer" class="card-footer">
      <slot name="footer"></slot>
    </div>
  </div>
</template>

<script setup>
defineProps({
  title: {
    type: String,
    default: ''
  },
  shadow: {
    type: Boolean,
    default: true
  }
})
</script>

<style scoped>
.base-card {
  background-color: white;
  border-radius: 8px;
  overflow: hidden;
  margin-bottom: 1rem;
}

.with-shadow {
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.card-header {
  padding: 1rem;
  border-bottom: 1px solid #e0e4e8;
}

.card-header h3 {
  margin: 0;
  color: #333;
}

.card-body {
  padding: 1rem;
}

.card-footer {
  padding: 1rem;
  border-top: 1px solid #e0e4e8;
  background-color: #f8f9fa;
}
</style>
