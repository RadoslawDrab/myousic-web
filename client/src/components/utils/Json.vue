<script setup lang="ts">
import { download } from '@/utils'
import { sanitizeObject } from '@/utils/object'
import { diffJson } from 'diff'
import useStatus from '@/composables/use-status'
import { useClipboard } from '@vueuse/core'

import { VCard } from 'vuetify/components'

interface Props extends /* @vue-ignore */ Partial<VCard['$props']> {
  copy?: boolean
  paste?: boolean
  export?: boolean
  import?: boolean
  cardTitle?: string
  contentClass?: string
  showDiff?: boolean
  maxContentHeight?: string | number
  fileName?: string
}

const props = withDefaults(defineProps<Props>(), {
  cardTitle: 'JSON',
  copy: false,
  paste: false,
  export: false,
  import: false
})

const cb = useClipboard()
const status = useStatus()

const emit = defineEmits<{
  import: [item: object]
  export: [item: object]
}>()

const item = defineModel<object>()
const prevItem = defineModel<object>('previous')

const importFile = reactive<{
  file?: File
  data?: object
  dialog: boolean
  replace: boolean
  isLoading: boolean
}>({
  dialog: false,
  replace: true,
  isLoading: false
})

const heightStyle = computed(() => {
  if (!props.maxContentHeight) return 'auto'
  return typeof props.maxContentHeight === 'number' ? `calc(2rem * ${Math.max(props.maxContentHeight, 1)})` : props.maxContentHeight
})

function getValue(value: string | object) {
  if (typeof value === 'string') {
    try {
      return JSON.parse(value)
    } catch {
      return {}
    }
  }
  return value
}

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

async function exportJson() {
  download(
      (props.fileName || 'export') + '.json',
      new Blob([JSON.stringify(item.value, null, 2)], { type: 'application/json' })
  )

  emit('export', item.value)
}
function importJson() {
  const obj = importFile.replace ? importFile.data : { ...getValue(item.value), ...importFile.data }

  item.value = obj
  importFile.dialog = false

  emit('import', obj)
}



watch(() => importFile.file, async (file) => {
  importFile.isLoading = true
  if (!file || file.type.toLowerCase() !== 'application/json') return importFile.data = null
  importFile.data = sanitizeObject(getValue(await file.text()), getValue(item.value))
  importFile.isLoading = false
}, { deep: true })
</script>

<template>
  <v-card flat v-bind="props">
    <v-card-text :class="props.contentClass">
      <span v-if="props.cardTitle" class="d-block text-h6">{{ props.cardTitle }}</span>
      <pre v-if="!props.showDiff || !prevItem" class="rounded pa-2 pa-sm-4 overflow-auto bg-black text-white" :style="{ maxHeight: heightStyle, minHeight: '2em' }">{{ JSON.stringify(item || {}, null, 2) }}</pre>
      <div v-else class="rounded pa-2 pa-sm-4 overflow-auto bg-black text-white" :style="{ height: heightStyle }">
        <template v-for="part in diffJson(prevItem, item)">
          <pre v-if="part.added" class="text-green">{{ part.value }}</pre>
          <pre v-else-if="part.removed" class="text-red">{{ part.value }}</pre>
          <pre v-else>{{ part.value }}</pre>
        </template>
      </div>
    </v-card-text>
    <v-card-actions v-if="props.copy || props.paste || props.export || props.import || $slots.appendActions || $slots.prependActions" class="flex-wrap border-t">
      <slot name="prependActions">
      </slot>
      <v-btn v-if="props.copy" prepend-icon="mdi-content-copy" flat @click="copyJson">Copy</v-btn>
      <v-btn v-if="props.paste" prepend-icon="mdi-content-paste" flat @click="pasteJson">Paste</v-btn>
      <v-btn v-if="props.export" prepend-icon="mdi-export" flat @click="exportJson">Export</v-btn>
      <v-btn v-if="props.import" prepend-icon="mdi-import" flat @click="importFile.dialog = !importFile.dialog">Import</v-btn>
      <v-dialog v-model="importFile.dialog" :max-width="700">
        <v-sheet>
          <v-form class="pa-2 pa-sm-4" @submit.prevent="importJson" :loading="importFile.isLoading" :disabled="importFile.isLoading">
            <Flex column>
              <span class="text-h4">Import</span>
              <v-divider />
              <Flex column>
                <v-file-input v-model="importFile.file" class="flex-grow-1" label="Import File" prepend-icon="" accept="application/json"></v-file-input>
                <v-checkbox-btn v-model="importFile.replace" label="Replace existing" />
              </Flex>
              <Json v-if="importFile.data" v-model="importFile.data" v-model:previous="item" content-class="pa-0" show-diff></Json>
              <Flex align="center">
                <v-btn prepend-icon="mdi-import" variant="tonal" color="primary" type="submit">Import</v-btn>
                <v-btn prepend-icon="mdi-close" variant="tonal" color="error" @click="importFile.dialog = false">Close</v-btn>
              </Flex>
            </Flex>
          </v-form>
        </v-sheet>
      </v-dialog>
      <slot name="appendActions">
      </slot>
    </v-card-actions>
  </v-card>
</template>