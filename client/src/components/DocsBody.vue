<script setup lang="ts">
  import { CacheReturn } from '@/composables/use-cache'
  import useMarkdown from '@/composables/use-markdown'
  import useStatus from '@/composables/use-status'
  import { formatTitle } from '@/utils/string'

  const status = useStatus()
  const title = useTitle()

  const currentDoc = defineModel<DocsData | null>({ required: true })
  const previousDoc = defineModel<DocsData | null>('previous')
  const nextDoc = defineModel<DocsData | null>('next')

  const props = defineProps<{
    cache: CacheReturn
    isLoading: boolean
  }>()

  const { text: docFileContent, html: docFileRender } = useMarkdown()

  watch(props.cache.data, (data) => {
    docFileContent.value = data || ''
  })

  watch(props.cache.error, (error) => {
    if (!error) return
    status.add({
      title: error,
      type: 'error'
    })
  })

  watch(currentDoc, (doc) => {
    if (!doc) return

    title.value = formatTitle(doc.title)
  })
</script>

<template>
  <Flex v-if="currentDoc" column>
    <Flex class="border-b" column>
      <Flex justify="space-between" align="center">
        <h1 class="text-h4">{{ currentDoc.title }}</h1>
      </Flex>
      <span v-if="currentDoc?.description" class="text-body-2">{{ currentDoc.description }}</span>
    </Flex>

    <div v-show="!props.isLoading" class="flex-grow-1 markdown-body">
      <div v-html="docFileRender"></div>
      <span v-if="!docFileRender" class="d-block ma-5 text-center text-body-1 text-grey">No content</span>
    </div>
    <v-skeleton-loader v-if="props.isLoading" type="article"></v-skeleton-loader>

    <Flex class="border-t pt-2 mt-4" justify="space-between">
      <v-btn v-if="previousDoc" prepend-icon="mdi-chevron-left" :append-icon="previousDoc.icon" :to="`/docs/${previousDoc.path}`">{{ previousDoc.title }}</v-btn>
      <div v-else></div>
      <v-btn v-if="nextDoc" append-icon="mdi-chevron-right" :prepend-icon="nextDoc.icon" :to="`/docs/${nextDoc.path}`">{{ nextDoc.title }}</v-btn>
      <div v-else></div>
    </Flex>
  </Flex>
</template>