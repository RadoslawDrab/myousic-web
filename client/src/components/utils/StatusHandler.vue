<script setup lang="ts">
import ProgressBar from '@/components/utils/ProgressBar.vue'

import useStatus, { StatusHandlerData } from '@/composables/use-status'
import { transition, promiseTimeout } from '@vueuse/core'

const props = withDefaults(defineProps<{
  time?: number | false
  transitionAnimTime?: number
  entryDelay?: number
  exitDelay?: number
}>(), {
  time: 5000,
  entryDelay: 0,
  transitionAnimTime: 200,
  exitDelay: 500
})

const status = useStatus()

const progressBar = useTemplateRef('progressBar')
const animProgress = ref<number>(0)
const progress = computed(() => progressBar.value?.animation || null)

/**
 * Computed property that returns the date associated with the status message
 * If the timestamp is false, returns null
 * If the timestamp is not defined, returns a new Date object
 */
const date = computed<Date | null>(() => {
  if (status.data?.timestamp === false) return null

  return status.data?.timestamp ? new Date(status.data.timestamp * 1000) : new Date()
})

/**
 * Function to run before removing the status message
 * Runs the animation of the progress bar from visible to hidden
 * Waits for the exit delay
 */
async function beforeRemove(status: StatusHandlerData | null) {
  await transition(animProgress, 1, 0, {
    easing: n => n,
    duration: props.transitionAnimTime
  })
  if (props.exitDelay > 0) await promiseTimeout(props.exitDelay)
}

/**
 * Function to show the status message
 * If the progress bar is defined, resets it
 * If there is an entry delay, waits for it
 * Animates the transition from hidden to visible
 * If the time is defined, starts the animation of the progress bar
 */
async function show(): Promise<void>
async function show(progress: InstanceType<typeof ProgressBar>['$data']['animation'], time: number): Promise<void>
async function show(progress?: InstanceType<typeof ProgressBar>['$data']['animation'], time?: number): Promise<void> {
  // Reset the progress bar
  progress && progress.reset()

  // If there is an entry delay, wait for it
  if (props.entryDelay > 0) await promiseTimeout(props.entryDelay)

  // Animate the transition from hidden to visible
  await transition(animProgress, 0, 1, {
    easing: n => n,
    duration: props.transitionAnimTime
  })

  // Start the animation of the progress bar
  progress && time && progress.start({
    duration: time,
    easing: 'linear'
  })
}

// Watch for changes in the status data and the progress bar
watch([() => status.data, progress], async ([data, progress]) => {
  // Get the time from the status data or the props
  const time = data?.time ?? props.time

  // If there is no time, show the status message without a progress bar
  if (time == false) {
    await show()
  }

  // If there is no progress bar, or no time, don't do anything
  if (!progress || !time) return

  // Show the status message with the given time
  await show(progress, time)
})
</script>

<template>
  <v-alert
      v-if="status.data"
      class="transition-control ma-2 z-9999"
      density="compact"
      position="fixed"
      :icon-size="20"
      location="bottom right"
      :color="status.data?.type"
      :icon="`$${status.data?.type}`"
      v-bind="status.data?.props"
  >
    <template #append>
      <v-btn
          v-if="status.data?.closable"
          @click="status.removeFirst(beforeRemove)"
          variant="text"
          density="compact"
          icon="mdi-close"
          size="small"
      >
      </v-btn>
    </template>
    <template #text>
      <p class="text-md font-weight-bold">
        {{ status.data?.title }}
      </p>
      <p>{{ (status.data?.text) }}</p>
      <p v-if="date" class="text-sm text-right">
        {{ date.toLocaleTimeString() }}
      </p>
      <ProgressBar
          ref="progressBar"
          v-if="status.data.time !== false"
          class-name="position-absolute bottom-0 left-0"
          :default-duration="props.time || 3000"
          :color="status.data?.type"
          :border="0"
          :height="4"
          @end="status.removeFirst(beforeRemove)"
      />
    </template>
  </v-alert>
</template>

<style scoped>
.transition-control {
  opacity: v-bind('animProgress');
  bottom: calc(5px * v-bind('animProgress')) !important;
}
</style>