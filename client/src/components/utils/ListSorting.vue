<script setup lang="ts" generic="T">
import { VueDraggable } from 'vue-draggable-plus'

const list = defineModel<T[]>({ required: true })
</script>

<template>
  <v-list density="compact" class="pa-0 bg-transparent">
    <VueDraggable v-model="list" ghost-class="opacity-30">
      <v-list-item v-for="(item, index) in list" class="cursor-grab pa-0 ma-0 mb-1 border">
        <slot :item="item" :index="index">
          {{ index + 1 }}.
          {{ item }}
        </slot>
      </v-list-item>
    </VueDraggable>
  </v-list>
</template>