<script setup lang="ts">
import * as uuid from 'uuid'

import useCache from '@/composables/use-cache'
import useSession from '@/composables/use-session'
import useStatus from '@/composables/use-status'

import { flattenRecursiveObject, mapRecursive } from '@/utils/array'
import { joinClass } from '@/utils/string'

import DocsBody from '@/components/DocsBody.vue'


const route = useRoute()

const status = useStatus()
const session = useSession<{ docs: DocsData[] }>({
  docs: []
}, 'DOCS')

const isLoading = ref<boolean>(false)


const currentDocPath = computed(() => (Array.isArray(route.params.doc) ? route.params.doc : [route.params.doc]).join('/') )

const docs = computed({
  get: () => session.value.docs || [],
  set: (v) => session.value.docs = v
})
const currentDoc = computed<DocsData | null>(() => {
  const flattened = flattenRecursiveObject(docs.value, 'id')
  if (!currentDocPath.value) {
    return flattened[0]
  }
  return flattened.find(doc => doc.path === currentDocPath.value) || null
})

const cache = useCache(computed(() => currentDoc.value?.file ? '/docs/' + currentDoc.value.file : null))

const previousDoc = computed(() => getRelativeDoc(-1))
const nextDoc = computed(() => getRelativeDoc(1))


function getRelativeDoc(deltaIndex: number, current: DocsData | null = currentDoc.value) {
  if (deltaIndex === 0) throw new Error('Delta cannot be 0')

  const flattenDocs = flattenRecursiveObject(docs.value, 'id')

  const index = flattenDocs.findIndex(doc => doc.id === current?.id)
  if (index == -1) return null
  const newIndex = index + deltaIndex
  if (newIndex < 0 || newIndex >= flattenDocs.length) return null

  const relativeDoc = flattenDocs[newIndex]

  if (!relativeDoc.file || !relativeDoc.path) return getRelativeDoc(deltaIndex + (deltaIndex > 0 ? 1 : -1))

  return relativeDoc
}

async function getDocumentsData() {
  try {
    isLoading.value = true
    const resp = await fetch('/docs/docs.json', { cache: 'no-cache' })
    docs.value = mapRecursive([...await resp.json()], (item: DocsData) => {
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

onMounted(async () => {
  if (docs.value.length) return
  await getDocumentsData()
})

definePage({
  meta: {
    title: 'Doc'
  }
})
</script>

<template>
  <Flex align="center" justify="space-between">
    <span class="d-block text-h5 text-sm-h4">Docs</span>
    <v-btn icon="mdi-refresh" @click="cache.refresh(); getDocumentsData()" variant="text" v-tooltip="'Refresh'" :loading="cache.isLoading.value"></v-btn>
  </Flex>
  <v-divider class="my-2" />
  <Flex>
    <DocsNav v-model="docs" />
    <div class="border pa-3 pa-sm-5 flex-grow-1" :class="joinClass(isLoading && 'bg-grey-darken-4')">
      <DocsBody
          v-model="currentDoc"
          v-model:previous="previousDoc"
          v-model:next="nextDoc"
          :cache="cache"
          :is-loading="isLoading"
      />
    </div>
  </Flex>
</template>