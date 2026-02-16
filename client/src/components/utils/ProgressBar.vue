<script setup lang="ts">
  import { useTheme } from 'vuetify'

  type Color = 'background' | 'surface' | 'primary' | 'secondary' | 'success' | 'warning' | 'error' | 'info'
  const props = withDefaults(defineProps<{
    height?: number | string
    color?: Color | string,
    bgColor?: Color | string,
    border?: string | number,
    defaultDuration?: number
    className?: string
  }>(), {
    height: 5,
    border: 1,
    defaultDuration: 3000,
    color: 'surface',
    bgColor: 'transparent',
  })

  const emit = defineEmits<{
    start: [animation: Animation],
    end: [],
  }>()

  const theme = useTheme()

  const backgroundColor = computed(() => theme.current.value.colors[props.bgColor] || props.bgColor)
  const color = computed(() => theme.current.value.colors[props.color] || props.color)

  const progressBar = useTemplateRef('progressBar')
  const progressBarFill = computed<HTMLDivElement | null>(() => progressBar.value ? progressBar.value.querySelector<HTMLDivElement>('.progress__fill') : null)
  const animation = ref<Animation | null>(null)

  function start(options?: KeyframeAnimationOptions) {
    if (!progressBarFill.value) return
    const anim = progressBarFill.value.animate([
      {
        width: '0',
      },
      {
        width: '100%'
      }
    ], {
      easing: 'linear',
      duration: props.defaultDuration,
      iterations: 1,
      fill: 'forwards',
      ...options
    })
    emit('start', anim)
    anim.addEventListener('finish', () => emit('end'))
    animation.value = anim
  }
  function resume() {
    if (!animation.value) return
    animation.value.play()
  }
  function stop() {
    if (!animation.value) return
    animation.value.pause()
  }
  function reset() {
    if (!animation.value) return
    animation.value.cancel()
  }

  defineExpose({
    animation: {
      value: animation,
      start,
      resume,
      stop,
      reset
    }
  })
</script>

<template>
  <div ref="progressBar" class="progress" :class="props.className">
    <div class="progress__fill"></div>
  </div>
</template>

<style scoped>
  .progress {
    position: relative;
    height: calc(max(v-bind('props.height') * 1px, 1px));
    width: 100%;
    background-color: v-bind('backgroundColor');
    border: calc(v-bind('props.border') * 1px) solid v-bind('color');
  }
  .progress .progress__fill {
    position: absolute;
    top: 0;
    left: 0;
    height: 100%;
    background-color: v-bind('color');
  }
</style>