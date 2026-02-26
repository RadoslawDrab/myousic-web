<script setup lang="ts">
import useCache from '@/composables/use-cache'
import useSession from '@/composables/use-session'
import { useRouteQuery } from '@vueuse/router'
import * as uuid from 'uuid'

import useMarkdown from '@/composables/use-markdown'
import { filterRecursive, flattenRecursiveObject, mapRecursive } from '@/utils/array'
import { formatTitle, joinClass } from '@/utils/string'

import useStatus from '@/composables/use-status'

import RecursiveListItem from '@/components/utils/RecursiveListItem.vue'

const session = useSession<{ docs: DocsData[] }>({
  docs: []
}, 'DOCS')

const status = useStatus()
const title = useTitle()
const { text: docFileContent, html: docFileRender } = useMarkdown()

const currentDocId = useRouteQuery<string>('id', '')

const isLoading = ref<boolean>(false)
const search = ref<string>('')

const docs = computed({
  get: () => session.value.docs || [],
  set: (v) => session.value.docs = v
})

const currentDoc = computed<DocsData | null>({
  get() {
    const flattened = flattenRecursiveObject(docs.value, 'id')
    if (!currentDocId.value) {
      return flattened[0]
    }
    return flattened.find(doc => doc.id === currentDocId.value) || null
  },
  set(value) {
    if (!value) return
    currentDocId.value = value.id
  }
})

const cache = useCache(computed(() => currentDoc.value?.file ? '/docs/' + currentDoc.value.file : null), { name: 'DOCS' })


const previousDoc = computed(() => getRelativeDoc(-1))
const nextDoc = computed(() => getRelativeDoc(1))

const filteredDocs = computed(() => {
  if (!search.value) return docs.value

  return filterRecursive(docs.value, (doc) => {
    const _search = new RegExp(search.value, 'i')

    return (
        !!doc.title.match(_search) ||
        !!doc?.description?.match(_search) ||
        !!doc?.fileContent?.match(_search)
    )
  })
})
const breadcrumbs = computed(() => {
  return flattenRecursiveObject(filterRecursive(docs.value, (doc) => doc.id === currentDoc.value.id), 'id')
    .map(doc => ({
        title: doc.title,
        disabled: doc.id === currentDoc.value?.id || !doc.file,
        to: `/docs?id=${doc.id}`
      })
    )
})


function getRelativeDoc(deltaIndex: number, current: DocsData | null = currentDoc.value) {
  if (deltaIndex === 0) throw new Error('Delta cannot be 0')

  const flattenDocs = flattenRecursiveObject(docs.value, 'id')

  const index = flattenDocs.findIndex(doc => doc.id === current?.id)
  if (index == -1) return null
  const newIndex = index + deltaIndex
  if (newIndex < 0 || newIndex >= flattenDocs.length) return null

  const relativeDoc = flattenDocs[newIndex]

  if (!relativeDoc.file) return getRelativeDoc(deltaIndex + (deltaIndex > 0 ? 1 : -1))

  return relativeDoc
}

async function getDocumentsData(): Promise<DocsData[]> {
  try {
    isLoading.value = true
    const resp = await fetch('/docs/docs.json', { cache: 'force-cache' })
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

watch(currentDoc, async (doc) => {
  if (!doc) return
  title.value = formatTitle(doc.title)
}, { immediate: true, deep: true })

watch(cache.data, (data) => {
  docFileContent.value = data || ''
})

watch(cache.error, (error) => {
  if (!error) return
  status.add({
    title: error,
    type: 'error'
  })
})
watch(cache.isLoading, (loading) => {
  isLoading.value = loading
})

onMounted(async () => {
  if (docs.value.length) return
  docs.value = await getDocumentsData()
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
  <Flex align="center" justify="space-between">
    <span class="d-block text-h5 text-sm-h4">Docs</span>
    <v-btn icon="mdi-refresh" @click="cache.refresh()" variant="text"></v-btn>
  </Flex>
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
                @click="doc?.file ? currentDoc = doc : currentDoc = getRelativeDoc(1, doc)"
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
    <div class="border pa-3 pa-sm-5 flex-grow-1" :class="joinClass(isLoading && 'bg-grey-darken-4')">
      <Flex v-if="currentDoc" column>
        <Flex class="border-b" column>
          <Flex justify="space-between" align="center">
            <h1 class="text-h4">{{ currentDoc.title }}</h1>
            <v-breadcrumbs :items="breadcrumbs" density="compact">
              <template #divider>
                  <v-icon icon="mdi-chevron-right"></v-icon>
              </template>
              <template #item="{ item, index }">
                <v-breadcrumbs-item :disabled="item.disabled" :to="item.to">
                  {{ item.title }}
                </v-breadcrumbs-item>
              </template>
            </v-breadcrumbs>
          </Flex>
          <span v-if="currentDoc?.description" class="text-body-2">{{ currentDoc.description }}</span>
        </Flex>

        <div v-show="!isLoading" class="flex-grow-1 markdown-body">
          <div v-html="docFileRender"></div>
          <span v-if="!docFileRender" class="d-block ma-5 text-center text-body-1 text-grey">No content</span>
        </div>
        <v-skeleton-loader v-if="isLoading" type="article"></v-skeleton-loader>

        <Flex class="border-t pt-2 mt-4" justify="space-between">
          <v-btn v-if="previousDoc" prepend-icon="mdi-chevron-left" @click="currentDoc = previousDoc">{{ previousDoc.title }}</v-btn>
          <div v-else></div>
          <v-btn v-if="nextDoc" append-icon="mdi-chevron-right" @click="currentDoc = nextDoc">{{ nextDoc.title }}</v-btn>
          <div v-else></div>
        </Flex>
      </Flex>
    </div>
  </Flex>
</template>