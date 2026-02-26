<script setup lang="ts">
  const value = defineModel<number>()
  const props = defineProps<{
    min: number
    max: number
    step: number | (number | { value: number, label?: string })[]
    inverted?: boolean
    label?: string
  }>()

  const steps = computed(() => {
    return (Array.isArray(props.step) ? props.step : [props.step])
      .map(step => typeof step === 'number' ? { label: step.toString(), value: step } : step)
      .sort((a, b) => props.inverted ? b.value - a.value : a.value - b.value)
  })

  function adjust(step: number) {
    value.value = Math.max(Math.min(value.value + step, props.max), props.min || 0)
  }
</script>

<template>
  <v-speed-dial :close-on-content-click="false">
    <template #activator="internalProps">
      <slot name="activator" :="internalProps">
        <v-btn prepend-icon="mdi-menu" variant="tonal" flat v-bind="internalProps.props">
          <slot name="activatorButton">{{ props.label || 'Clipping' }}</slot>
        </v-btn>
      </slot>
    </template>
    <v-sheet class="pa-2">
      <Flex column>
        <v-btn-group v-for="step in steps" :key="step.value" variant="outlined" direction="vertical">
          <v-btn class="text-none" prepend-icon="mdi-chevron-up" @click="adjust(step.value)" :disabled="value + step.value >= props.max">
            <slot name="button" :step="step">{{ step.label || step.value }}</slot>
          </v-btn>
          <v-btn class="text-none" prepend-icon="mdi-chevron-down" @click="adjust(-step.value)" :disabled="value - step.value <= props.min">
            <slot name="button" :step="step">{{ step.label || step.value }}</slot>
          </v-btn>
        </v-btn-group>
      </Flex>
    </v-sheet>
  </v-speed-dial>
</template>