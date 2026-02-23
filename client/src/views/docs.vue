<script setup lang="ts">
import useData from '@/composables/use-data'
import { filterRecursive, flattenRecursive, flattenRecursiveObject, mapRecursive } from '@/utils/array'
import { formatTitle, joinClass } from '@/utils/string'
import * as uuid from 'uuid'
import { marked } from 'marked'

import useStatus from '@/composables/use-status'

import RecursiveListItem from '@/components/utils/RecursiveListItem.vue'


const { session } = useData()
const status = useStatus()
const title = useTitle()

const currentDoc = ref<DocsData | null>(null)
const isLoading = ref<boolean>(true)
const search = ref<string>('')

function getRelativeDoc(deltaIndex: number) {
  if (deltaIndex === 0) throw new Error('Delta cannot be 0')

  const docs = session.value.cachedDocs || []

  const flattenDocs = flattenRecursiveObject(docs, 'id')

  const index = flattenDocs.findIndex(doc => doc.id === currentDoc.value?.id)
  if (index == -1) return null
  const newIndex = index + deltaIndex
  if (newIndex < 0 || newIndex >= flattenDocs.length) return null

  return flattenDocs[newIndex]
}
const previousDoc = computed(() => getRelativeDoc(-1))
const nextDoc = computed(() => getRelativeDoc(1))

const filteredDocs = computed(() => {
  if (!search.value) return session.value.cachedDocs || []

  return filterRecursive(session.value.cachedDocs || [], (doc) => {
    const _search = new RegExp(search.value, 'i')

    return (
        !!doc.title.match(_search) ||
        !!doc?.description?.match(_search) ||
        !!doc?.fileContent?.match(_search)
    )
  })
})


async function getDocumentsData(): Promise<DocsData[]> {
  try {
    isLoading.value = true
    const resp = await fetch('/docs/docs.json')
    return mapRecursive([...await resp.json()], (item: DocsData) => {
      if (item.id) return item
      return {
        id: uuid.v4(),
        ...item
      }
    })

  } catch (e) {
    console.error(e)
    status.add({
      title: e,
      type: 'error'
    })
  } finally {
    isLoading.value = false
  }
}

async function render(data: DocsData) {
  try {
    isLoading.value = true
    const resp = await fetch(`/docs/${data.file}`, { cache: 'force-cache' })
    return marked.parse(await resp.text())

  } catch (e) {
    console.error(e)
    status.add({
      title: e,
      type: 'error'
    })
  } finally {
    isLoading.value = false
  }

}

watch(currentDoc, async (doc) => {
  title.value = formatTitle(currentDoc.value.title)
  if (doc.fileContent) return

  currentDoc.value.fileContent = await render(doc)
}, { deep: true })

onMounted(async () => {
  const docs = await getDocumentsData()
  session.value.cachedDocs = docs
  if (docs.length) currentDoc.value = docs[0]
})

definePage({
  meta: {
    title: 'Docs',
    icon: 'mdi-file-document',
    includeInNav: true,
    order: 100
  }
})
</script>

<template>
  <span class="d-block text-h5 text-sm-h4">Docs</span>
  <v-divider class="my-2" />
  <Flex>
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
                :active="doc?.id === currentDoc?.id"
                :style="{ 'padding-left': (indent + 1) * 1.5 + 'rem', 'padding-right': '1.5rem' }"
                variant="text"
                active-color="primary"
                @click="currentDoc = doc"
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
          <template></template>
        </RecursiveListItem>
        <span v-if="!filteredDocs.length" class="d-block pa-4 text-body-1 text-grey">Nothing found</span>
      </v-list>
    <div class="border pa-3 pa-sm-5 flex-grow-1" :class="joinClass(isLoading && 'bg-grey-darken-4')">
      <span v-if="!currentDoc" class="d-block ma-5 text-center text-body-1 text-grey">No doc selected</span>
      <template v-if="currentDoc">
        <h1 class="text-h4">{{ currentDoc.title }}</h1>
        <span v-if="currentDoc?.description" class="d-block text-body-2 my-2">{{ currentDoc.description }}</span>
        <v-divider />

        <div v-if="!isLoading" class="markdown-body" v-html="currentDoc?.fileContent"></div>
        <v-skeleton-loader v-else type="article"></v-skeleton-loader>

        <Flex class="border-t pt-2" justify="space-between">
          <v-btn v-if="previousDoc" prepend-icon="mdi-chevron-left" @click="currentDoc = previousDoc">{{ previousDoc.title }}</v-btn>
          <div v-else></div>
          <v-btn v-if="nextDoc" append-icon="mdi-chevron-right" @click="currentDoc = nextDoc">{{ nextDoc.title }}</v-btn>
          <div v-else></div>
        </Flex>
      </template>
    </div>
  </Flex>
</template>