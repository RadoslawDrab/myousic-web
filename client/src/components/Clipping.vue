<script setup lang="ts">

import ClippingButtons from '@/components/ClippingButtons.vue'

const item = defineModel<Partial<ExtendedTrack>>()

const props = withDefaults(defineProps<{
  sliderStep?: number
  step?: number | (number | { value: number, label?: string })[]
}>(), {
  sliderStep: 1000,
  step: () => [
    { label: '5ms', value: 5 },
    { label: '50ms', value: 50 },
    { label: '100ms', value: 100 },
    { label: '250ms', value: 250 },
    { label: '500ms', value: 500 },
    { label: '1s', value: 1000 },
    { label: '5s', value: 5000 }
  ]
})

const max = computed(() => Math.min(item.value?.trackTimeMillis || 0))

function formatTime(ms: number) {
  const mins = Math.floor(ms / 60000).toString().padStart(2, '0')
  const secs = Math.floor((ms % 60000) / 1000).toString().padStart(2, '0')
  const millis = (Math.round(ms % 1000)).toString().padStart(3, '0')
  return `${mins}:${secs}:${millis}`
}

watch(() => item.value.clipping, (clipping) => {
  if (clipping) return

  item.value.clipping = [0, item.value.trackTimeMillis || 0]
}, { immediate: true })

</script>

<template>
  <Flex class="my-2" justify="center" align="center" v-if="item.clipping">
    <ClippingButtons
        v-model="item.clipping[0]"
        :min="0"
        :max="Math.min(max, item.clipping[1])"
        :step="props.step"
        label="Start"
    />
  <span>{{ formatTime(item.clipping[0]) }}</span>
  <v-range-slider
      v-model="item.clipping"
      :step="sliderStep"
      :min="0"
      :max="max"
      strict
      flat
      hide-details
  ></v-range-slider>
  <span>{{ formatTime(item.clipping[1]) }}</span>
  <ClippingButtons
      v-model="item.clipping[1]"
      :min="item.clipping[0]"
      :max="max"
      :step="props.step"
      label="End"
  />
  </Flex>
</template>