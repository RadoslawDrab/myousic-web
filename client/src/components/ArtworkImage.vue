<script setup lang="ts">

import { getArtworkUrl } from '@/utils/api'

const props = withDefaults(defineProps<{
  url?: string
  src?: string
  placeholder?: string
  maxWidth?: number | string
  minWidth?: number | string
  smallClass?: string
  largeClass?: string
  smallRenderSize?: number
  largeRenderSize?: number
}>(), {
  smallRenderSize: 250,
  largeRenderSize: 1000,
  placeholder: 'https://images.placeholders.dev/?width=300&height=300&text=No Image'
})

const src = computed(() => ({
  small: props.src || getArtworkUrl(props.url, props.smallRenderSize) || props.placeholder,
  large: props.src || getArtworkUrl(props.url, props.largeRenderSize) || props.placeholder
}))

function getSize(size: string | number, defaultValue: string = 'auto') {
  if (typeof size === 'number') return size + 'px'
  return size || defaultValue
}
</script>

<template>
  <v-dialog max-height="80vh" max-width="80vw" close-on-back close-on-content-click>
    <template #activator="{ props: internalProps }">
      <v-img
          v-if="props.url"
          class="cursor-pointer w-100"
          :class="props.smallClass"
          :style="{ 'max-width': getSize(props.maxWidth), 'min-width': getSize(props.minWidth) }"
          :lazy-src="props.placeholder"
          :src="src.small"
          v-bind="internalProps"
      />
    </template>
    <v-img
        v-if="props.url"
        :class="props.largeClass"
        style="height: 80vh;"
        :lazy-src="props.placeholder"
        :src="src.large"
    ></v-img>
  </v-dialog>
</template>