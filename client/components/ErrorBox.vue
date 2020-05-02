<template>
  <div class="error-box">
    <strong>Error:</strong>
    <slot></slot>
  </div>
</template>

<style scoped>
  .error-box
  {
    background-color: rgba(255, 100, 100, 0.4);
    border: 2px solid #bb0000;
    border-radius: 4px;
  }
</style>