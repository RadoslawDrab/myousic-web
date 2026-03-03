<script setup lang="ts">
import { filterRecursive } from '@/utils/array'

import RecursiveListItem from '@/components/utils/RecursiveListItem.vue'

const docs = defineModel<DocsData[]>()

const search = ref<string>('')

const filteredDocs = computed(() => {
  if (!search.value) return docs.value

  return filterRecursive(docs.value, (doc) => {
    const _search = new RegExp(search.value, 'i')

    return (
        !!doc.title.match(_search) ||
        !!doc?.description?.match(_search) ||
        (doc.tags || []).includes(search.value)
    )
  })
})

</script>

<template>
  <v-list class="bg-transparent py-0 align-self-start" style="min-width: 20%" border>
    <v-list-item class="border-b bg-grey-darken-4 py-3">
      <Flex wrap align="center" :gap="4">
        <v-icon icon="mdi-magnify"></v-icon>
        <v-text-field v-model="search" variant="plain" label="Search" placeholder="String or RegEx" min-width="100" persistent-placeholder></v-text-field>
      </Flex>
    </v-list-item>
    <RecursiveListItem :items="filteredDocs" v-slot="{ item: doc, indent, index }">
      <v-divider v-if="index > 0 && indent == 0" />
      <v-list-item
          class="bg-transparent"
          :style="{ 'padding-left': (indent + 1) * 1.5 + 'rem', 'padding-right': '1.5rem' }"
          variant="text"
          color="primary"
          :to="doc.path ? '/docs/' + doc.path : ''"
      >
        <Flex align="center">
          <v-icon :icon="doc.icon || 'mdi-chevron-right'"></v-icon>
          <Flex column :gap="1" class="text-body-1">
            <span>{{ doc?.title || 'Title' }}</span>
            <span v-if="doc?.description" class="text-gray" style="font-size: 0.75em">{{ doc.description }}</span>
          </Flex>
        </Flex>
      </v-list-item>
      <v-divider v-if="indent == 0" />
    </RecursiveListItem>
    <span v-if="!filteredDocs.length" class="d-block pa-4 text-body-1 text-grey">Nothing found</span>
  </v-list>
</template>