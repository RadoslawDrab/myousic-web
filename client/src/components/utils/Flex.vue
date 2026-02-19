<script setup lang="ts">
  import { joinClass } from '@/utils/string'

  type Breakpoint = '' | 'sm-' | 'md-' | 'lg-' | 'xl-'
  type Gap = VariableText<'0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9' | '10' | '11' | '12' | '13' | '14' | '15', Breakpoint>
  type Justify = VariableText<'start' | 'end' | 'center' | 'space-between' | 'space-around' | 'space-evenly', Breakpoint>
  type Align = VariableText<'start' | 'end' | 'center' | 'baseline' | 'stretch', Breakpoint>
  const props = withDefaults(defineProps<{
    column?: boolean
    reversed?: boolean
    gap?: number | Gap | Gap[]
    justify?: Justify | Justify[]
    align?: Align | Align[]
    wrap?: boolean
    grow?: boolean
    shrink?: boolean
    class?: string | string[]
  }>(), {
    gap: () => ['1', 'sm-2']
  })

  function getValue<T extends string | number>(value: T | T[], prefix: string) {
    return joinClass(...(Array.isArray(value) ? value : [value]).map(v => `${prefix}${v}`))
  }
  const classes = joinClass(
      'd-flex',
      (props.column ? 'flex-column' : 'flex-row') + (props.reversed ? '-reversed' : ''),
      props.gap !== undefined && getValue(props.gap, 'ga-'),
      props.wrap && 'flex-wrap',
      props.justify && getValue(props.justify, 'justify-'),
      props.align && getValue(props.align, 'align-'),
      props.grow && 'flex-grow-1',
      props.shrink && 'flex-shrink-1',
      ...(Array.isArray(props.class) ? props.class : [props.class])
  )
</script>

<template>
  <div :class="classes" class="">
    <slot></slot>
  </div>
</template>

<style scoped>

</style>