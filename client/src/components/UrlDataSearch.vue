<script setup lang="ts">
  import useData from '@/composables/use-data'
  import useFetch from '@/composables/use-fetch'

  const sessionData = useData()


  const props = defineProps<{
    formClass?: string
  }>()

  const { get, isLoading } = useFetch({ })

  const emit = defineEmits<{
    result: [result: API_SearchUrlResult]
  }>()

  async function onSubmit() {
    sessionData.value.result = null
    await nextTick()
    const response = await get<API_SearchUrlResult>(null, {
      query: {
        url: sessionData.value.url
      }
    })

    if (!response) return
    sessionData.value.result = response
    sessionData.value.search = (response.artist && response.title) ? `${response.artist} - ${response.title}` : response.fullTitle
    emit('result', response)

  }

  watch(() => sessionData.value.url, (url) => {
    if (!url) {
      sessionData.value.result = null
      return
    }
  }, { immediate: true })
</script>

<template>
    <p v-if="sessionData.result" class="text-sm-body-2 text-grey-darken-1 mb-1">{{ sessionData.result.fullTitle }}</p>
    <v-form
        class="d-flex align-center ga-2"
        :class="props.formClass"
        :disabled="isLoading"
        @submit.prevent="onSubmit"
    >
      <v-text-field v-model="sessionData.url" placeholder="Youtube URL" hide-details clearable></v-text-field>
      <v-btn v-tooltip="'Search URL data'" icon="mdi-magnify" variant="text" type="submit" rounded="sm" flat />
    </v-form>
</template>