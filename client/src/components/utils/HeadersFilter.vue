<script setup lang="ts">
import { useRouteQuery } from '@vueuse/router'
import * as uuid from 'uuid'
import { flattenRecursiveObject, mapRecursive } from '@/utils/array'

import HeadersCheckbox from '@/components/utils/HeadersCheckbox.vue'
import { VSheet } from 'vuetify/components'

const activeHeaders = defineModel<DataTableHeader[]>({ required: true })
const allHeaders = defineModel<DataTableHeader[]>('allHeaders', { required: true })

const props = defineProps<{
  btnClass?: string
  title?: string
  sheetProps?: InstanceType<typeof VSheet>['$props']
}>()


const queryFilter = useRouteQuery<string>('filter', '')
const filter = computed({
  get() {
    return queryFilter.value.split(';').filter(Boolean)
  },
  set(newValue) {
    queryFilter.value = newValue.join(';')
  }
})

const filterActive = computed(() => filter.value.length > 0)

const visualOrder = computed(() => flattenRecursiveObject(allHeaders.value, 'key').map(h => h.key))

function getActive(valueComparer?: boolean | ((header: DataTableHeader) => boolean)) {
  function _getActive(headers: DataTableHeader[], valueComparer?: boolean | ((header: DataTableHeader) => boolean)) {
    let active: DataTableHeader[] = []

    headers.forEach(header => {
      const show = (() => {
        const defaultShow = header.defaultShow !== false
        if (valueComparer !== undefined && header.removable !== true) {
          return (typeof valueComparer === 'function' ? valueComparer(header) : valueComparer)
        }

        return defaultShow

      })()

      if (show && !header.disabled) active.push(header)
      if (header.children) {
        active = [...active, ..._getActive(header.children, valueComparer)]
      }
    })

    return active
  }

  return _getActive(allHeaders.value, valueComparer)
}

function resetToDefault() {
  activeHeaders.value = getActive()
}

function toggleAll(value?: boolean) {
  activeHeaders.value = getActive(value !== undefined ? value : !filterActive.value)
}
function init() {
  if (filter.value.length > 0) {

    const sortedAll = [...allHeaders.value].sort((a, b) => {
      const indexA = filter.value.indexOf(a.key)
      const indexB = filter.value.indexOf(b.key)

      // If both are in the filter, sort by filter index
      if (indexA !== -1 && indexB !== -1) return indexA - indexB

      // If only one is in the filter, move it to the front
      if (indexA !== -1) return -1
      if (indexB !== -1) return 1

      // Otherwise maintain original order for non-active headers
      return 0
    })

    allHeaders.value = mapRecursive(sortedAll, (item) => ({
      ...item,
      id: uuid.v4()
    }))

    nextTick(() => {
      const rawActive = getActive((header) => filter.value.includes(header.key))

      // Sort the active headers to match the order in the URL filter
      activeHeaders.value = rawActive.sort((a, b) => {
        return filter.value.indexOf(a.key) - filter.value.indexOf(b.key)
      })
    })
  } else {
    activeHeaders.value = getActive()
  }
}

watch(activeHeaders, (activeHeaders) => {
  filter.value = flattenRecursiveObject(activeHeaders, 'key').map(h => h.key)
}, { deep: true })


onMounted(init)

defineExpose({
  resetToDefault,
  toggleAll,
  init
})

</script>

<template>
  <v-speed-dial location="bottom right" transition="slide-y-transition" :close-on-content-click="false">
    <template #activator="{ props: activatorProps }">
      <v-btn :class="props.btnClass" variant="text" rounded="sm" icon="mdi-filter" flat v-bind="activatorProps">
      </v-btn>
    </template>
    <v-sheet class="pa-4" key="content" :width="300" max-height="75vh" max-width="30vw" v-bind="props.sheetProps">
      <slot name="title">{{ props.title || '' }}</slot>
      <div class="d-flex justify-space-between ga-2 flex-wrap">
        <v-btn flat @click="resetToDefault" prepend-icon="mdi-restore">Reset</v-btn>
        <v-btn flat @click="toggleAll()" prepend-icon="mdi-check-all">
          {{ filterActive ? 'Check All' : 'Clear All' }}
        </v-btn>
      </div>
      <v-divider class="my-2"/>
      <HeadersCheckbox
          v-model="activeHeaders"
          v-model:all-headers="allHeaders"
          :visual-order="visualOrder"
      />
    </v-sheet>
  </v-speed-dial>
</template>