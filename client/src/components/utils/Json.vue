<script setup lang="ts">
import { diffJson } from 'diff'
import useStatus from '@/composables/use-status'
import { useClipboard } from '@vueuse/core'

import { VCard } from 'vuetify/components'

interface Props extends /* @vue-ignore */ Partial<VCard['$props']> {
  copy?: boolean
  paste?: boolean
  cardTitle?: string
  contentClass?: string
  showDiff?: boolean
  maxContentHeight?: string | number
}

const props = withDefaults(defineProps<Props>(), {
  cardTitle: 'JSON',
  copy: true,
  paste: true
})

const item = defineModel<any>()
const prevItem = defineModel<any>('previous')

const cb = useClipboard()
const status = useStatus()

async function copyJson() {
  await cb.copy(JSON.stringify(item.value, null, 2))
  status.add({ title: 'Copied to clipboard', type: 'success' })
}
async function pasteJson() {
  try {
    item.value = JSON.parse(cb.text.value)
    status.add({ title: 'Pasted from clipboard', type: 'success' })
  } catch (e) {
    console.error(e)
    status.add({ title: 'Failed to parse JSON', type: 'error' })
  }
}

const heightStyle = computed(() => {
  if (!props.maxContentHeight) return 'auto'
  return typeof props.maxContentHeight === 'number' ? `calc(2rem * ${Math.max(props.maxContentHeight, 1)})` : props.maxContentHeight
})
</script>

<template>
  <v-card flat v-bind="props">
    <v-card-text :class="props.contentClass">
      <span v-if="props.cardTitle" class="d-block text-h6">{{ props.cardTitle }}</span>
      <pre v-if="!props.showDiff || !prevItem" class="rounded pa-4 overflow-auto bg-black text-white" :style="{ maxHeight: heightStyle, minHeight: '2em' }">{{ JSON.stringify(item || {}, null, 2) }}</pre>
      <div v-else class="rounded pa-4 overflow-auto bg-black text-white" :style="{ height: heightStyle }">
        <template v-for="part in diffJson(prevItem, item)">
          <pre v-if="part.added" class="text-green">{{ part.value }}</pre>
          <pre v-else-if="part.removed" class="text-red">{{ part.value }}</pre>
          <pre v-else>{{ part.value }}</pre>
        </template>
      </div>
    </v-card-text>
    <v-card-actions v-if="props.copy || props.paste || $slots.appendActions || $slots.prependActions">
      <slot name="prependActions">
      </slot>
      <v-btn v-if="props.copy !== false" prepend-icon="mdi-content-copy" flat @click="copyJson">Copy</v-btn>
      <v-btn v-if="props.paste !== false" prepend-icon="mdi-content-paste" flat @click="pasteJson">Paste</v-btn>
      <slot name="appendActions">
      </slot>
    </v-card-actions>
  </v-card>
</template>