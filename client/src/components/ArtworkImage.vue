<script setup lang="ts">

import { getArtworkUrl } from '@/utils/api'

const props = withDefaults(defineProps<{
  url: string
  size?: number | string
  smallRenderSize?: number
  largeRenderSize?: number
}>(), {
  smallRenderSize: 250,
  largeRenderSize: 1000
})

const size = computed(() => {
  if (typeof props.size === 'number') return props.size + 'px'
  return props.size || '250px'
})
</script>

<template>
  <v-dialog max-height="80vh" max-width="80vw" close-on-back close-on-content-click>
    <template #activator="{ props: internalProps }">
      <v-img
          v-if="props.url"
          class="cursor-pointer w-100"
          :style="{ 'max-width': size, }"
          :src="getArtworkUrl(props.url, props.smallRenderSize)"
          v-bind="internalProps"
      />
    </template>
    <v-img v-if="props.url" style="height: 80vh;" :src="getArtworkUrl(props.url, props.largeRenderSize)"></v-img>
  </v-dialog>
</template>