<script setup lang="ts">
  import useData from '@/composables/use-data'
  import useFetch from '@/composables/use-fetch'

  const { session } = useData()


  const props = defineProps<{
    formClass?: string
  }>()

  const { get, isLoading } = useFetch({ })

  const emit = defineEmits<{
    result: [result: API_SearchUrlResult]
  }>()

  async function onSubmit() {
    session.value.result = null
    await nextTick()
    const response = await get<API_SearchUrlResult>(null, {
      path: ['yt-data'],
      query: {
        url: session.value.url
      }
    })

    if (!response) return
    session.value.result = response
    session.value.search = (response.artist && response.title) ? `${response.artist} - ${response.title}` : response.fullTitle
    emit('result', response)

  }

  watch(() => session.value.url, (url) => {
    if (!url) {
      session.value.result = null
      return
    }
  }, { immediate: true })
</script>

<template>
  <Flex column>
    <v-btn v-if="session.result" class="align-self-start text-none text-left text-body-2 text-grey-darken-1 mb-1" :href="session.url" target="_blank" density="compact" variant="text" flat>{{ session.result.fullTitle }}</v-btn>
    <v-form
        class="d-flex align-center ga-1 ga-sm-2"
        :class="props.formClass"
        :disabled="isLoading"
        @submit.prevent="onSubmit"
    >
      <v-text-field v-model="session.url" placeholder="Youtube URL" clearable></v-text-field>
      <v-btn v-tooltip="'Search URL data'" icon="mdi-magnify" variant="text" type="submit" rounded="sm" flat />
    </v-form>
  </Flex>
</template>