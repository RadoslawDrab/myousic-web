<script setup lang="ts">
  import { joinClass } from '@/utils/string'

  const props = defineProps<{
    column?: boolean
    reversed?: boolean
    gap?: number
    justify?: string
    align?: string
    wrap?: boolean
    class?: string | string[]
  }>()

  const classes = joinClass(
      'd-flex',
      (props.column ? 'flex-column' : 'flex-row') + (props.reversed ? '-reversed' : ''),
      props.gap !== undefined && `ga-${props.gap}`,
      props.wrap && 'flex-wrap',
      props.justify && `justify-${props.justify}`,
      props.align && `align-${props.align}`,
      ...(Array.isArray(props.class) ? props.class : [props.class])
  )
</script>

<template>
  <div :class="classes">
    <slot></slot>
  </div>
</template>

<style scoped>

</style>