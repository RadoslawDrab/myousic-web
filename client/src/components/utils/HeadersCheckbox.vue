<script setup lang="ts">

import { VueDraggable } from 'vue-draggable-plus'

const activeHeaders = defineModel<DataTableHeader[]>({ required: true })
const allHeaders = defineModel<DataTableHeader[]>('allHeaders', { required: true })

const props = withDefaults(defineProps<{
  parent?: DataTableHeader
  btnClass?: string,
  indent?: number
  indentMultiplier?: number
  indentUnit?: string
  visualOrder?: string[]
}>(), {
  indent: 0,
  indentUnit: 'em',
  indentMultiplier: 1
})


function isChecked(header: DataTableHeader) {
  return activeHeaders.value.some(h => h.id === header.id)
}

function toggleHeader(header: DataTableHeader, isEnabled: boolean) {
  if (isEnabled) {
    // Add if not present
    if (!isChecked(header)) {
      sortHeaders([...activeHeaders.value, header])
    }
  } else {
    // Remove if present
    sortHeaders(activeHeaders.value.filter(h => h.id !== header.id))
  }
}


function sortHeaders(unsortedHeaders?: DataTableHeader[]) {
  activeHeaders.value = (unsortedHeaders || [...activeHeaders.value]).sort((a, b) => {
    return props.visualOrder.indexOf(a.key) - props.visualOrder.indexOf(b.key)
  })
}

watch(allHeaders, (headers) => {
  sortHeaders()
}, { deep: true })

</script>

<template>
  <VueDraggable v-model="allHeaders" ghost-class="opacity-30">
    <div
        v-for="header in allHeaders"
        :key="header.key"
        :style="{ marginLeft: (props.indent * props.indentMultiplier) + props.indentUnit }"
    >
      <div
          v-if="header.hide !== true"
          class="d-flex align-center"
      >
        <v-icon icon="mdi-drag" class="cursor-grab"/>
        <v-checkbox-btn
            :model-value="isChecked(header)"
            :label="header.title"
            :disabled="header.removable === false || header.disabled"
            @update:model-value="val => toggleHeader(header, val)"
        />
      </div>
      <div v-if="header.children">
        <HeadersCheckbox
            v-model="activeHeaders"
            v-model:all-headers="header.children"
            :parent="header"
            :indent="props.indent + 1"
            :visual-order="visualOrder"
        />
        <v-divider class="my-1"/>
      </div>
    </div>
  </VueDraggable>
</template>