<script setup lang="ts">
  const value = defineModel<string>('value')
</script>

<template>
  <v-icon v-if="value === 'explicit'" v-tooltip="'Explicit'" icon="mdi-alpha-e-box" color="red"></v-icon>
  <v-icon v-else-if="value === 'cleaned'" v-tooltip="'Cleaned'" icon="mdi-alpha-c-box" color="yellow"></v-icon>
  <v-icon v-else v-tooltip="'Not Explicit'" icon="mdi-alpha-n-box" color="green"></v-icon>
</template>