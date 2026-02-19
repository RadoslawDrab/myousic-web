<script setup lang="ts">

import { getArtworkUrl } from '@/utils/api'

const props = withDefaults(defineProps<{
  url: string
  src?: string
  maxWidth?: number | string
  minWidth?: number | string
  smallClass?: string
  largeClass?: string
  smallRenderSize?: number
  largeRenderSize?: number
}>(), {
  smallRenderSize: 250,
  largeRenderSize: 1000
})

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
          :src="props.src || getArtworkUrl(props.url, props.smallRenderSize)"
          v-bind="internalProps"
      />
    </template>
    <v-img v-if="props.url" :class="props.largeClass" style="height: 80vh;" :src="props.src || getArtworkUrl(props.url, props.largeRenderSize)"></v-img>
  </v-dialog>
</template>