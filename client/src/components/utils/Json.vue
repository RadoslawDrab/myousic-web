<script setup lang="ts">
import useStatus from '@/composables/use-status'
import { useClipboard } from '@vueuse/core'

import { VCard } from 'vuetify/components'

interface Props extends /* @vue-ignore */ Partial<VCard['$props']> {
  copy?: boolean
  paste?: boolean
  cardTitle?: string
  contentClass?: string
}

const props = withDefaults(defineProps<Props>(), {
  cardTitle: 'JSON',
  copy: true,
  paste: true
})

const item = defineModel<any>()
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
    status.add({ title: 'Failed to parse JSON', type: 'error' })
  }
}
</script>

<template>
  <v-card flat v-bind="props">
    <v-card-text :class="props.contentClass">
      <span class="text-h6">{{ props.cardTitle }}</span>
      <pre class="rounded pa-4 overflow-x-auto bg-black text-white">{{ JSON.stringify(item, null, 2) }}</pre>
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