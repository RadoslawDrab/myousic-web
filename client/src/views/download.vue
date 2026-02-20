<script setup lang="ts">
  import useApi from '@/composables/use-api'
  import useData from '@/composables/use-data'
  import useSave from '@/composables/use-save'
  import { breakpointsVuetifyV3 } from '@vueuse/core'
  import { SubmitEventPromise } from 'vuetify/framework'

  const br = useBreakpoints(breakpointsVuetifyV3)

  const { session, local } = useData()
  const { renderComment, downloadTrack } = useApi()

  const track = ref<Partial<ExtendedTrack>>(session.value.savedTrack || {
    comment: local.value.defaultComment
  })
  const { draft, save, reset, isChanged } = useSave(track)

  const artworkFile = ref<File | null>(null)
  const objectUrl = ref<string | null>(null)

  const artworkUrl = computed(() => {
    return objectUrl.value || draft.value.artworkUrl100
  })
  const releaseDate = computed({
    get() {
      if (!draft.value.releaseDate) return new Date().getFullYear()
      return new Date(draft.value.releaseDate).getFullYear()
    },
    set(value) {
      draft.value.releaseDate = new Date(value + '-01-01').toISOString()
    }
  })

  async function onSubmit(e: SubmitEventPromise) {
    const status = await e
    if (!status.valid) return
    await downloadTrack(session.value.url, track.value, { artworkFile: artworkFile.value })
  }

  watch(() => session.value.result, (searchResult, prevSearchResult) => {
    if (!searchResult || searchResult.id === prevSearchResult?.id) return

    draft.value.artistName = searchResult.artist
    draft.value.trackName = searchResult.title
    draft.value.collectionName = searchResult.title + ' - Single'
    draft.value.artworkUrl100 = searchResult.artworkUrl

    if (searchResult.releaseDate) {
      draft.value.releaseDate = new Date(searchResult.releaseDate).toISOString()
    } else {
      const date = new Date(`${new Date().getFullYear()}-01-01`)
      draft.value.releaseDate = date.toISOString()
    }
  }, { immediate: true, deep: true })

  watch(track, (track) => {
    session.value.savedTrack = track
  }, { deep: true })

  watch(artworkFile, (newFile) => {
    if (objectUrl.value) URL.revokeObjectURL(objectUrl.value)

    if (newFile) {
      objectUrl.value = URL.createObjectURL(newFile)
    } else {
      objectUrl.value = null
    }
  })

  definePage({
    meta: {
      title: 'Download'
    }
  })
</script>

<template>
  <v-form class="d-flex flex-column ga-2" @submit.prevent="onSubmit">
    <UrlDataSearch />
    <Flex class="flex-column flex-md-row">
      <Flex column grow>
        <v-text-field v-model="draft.artistName" label="Artist Name"></v-text-field>
        <v-text-field v-model="draft.trackName" label="Track Name"></v-text-field>
        <v-text-field v-model="draft.collectionName" label="Album Name"></v-text-field>
        <v-number-input v-model="releaseDate" label="Release Date" :max="new Date().getFullYear()"></v-number-input>
        <Flex class="flex-column flex-sm-row">
          <v-text-field v-model="draft.primaryGenreName" label="Primary Genre" />
          <v-combobox v-model:model-value="draft.genres" label="Genres" chips closable-chips multiple></v-combobox>
        </Flex>
        <Flex class="flex-column flex-sm-row">
          <v-text-field v-model="draft.artworkUrl100" label="Artwork URL" :disabled="!!artworkFile"></v-text-field>
          <v-file-input v-model="artworkFile" label="Artwork File" accept="image/*" prepend-icon=""></v-file-input>
        </Flex>
      </Flex>
      <Flex column align="center" justify="center">
        <ArtworkImage :min-width="br.isGreater('sm') ? 400 : 200" :max-width="500" :url="artworkUrl" :small-render-size="500" :large-render-size="1000" />
      </Flex>
    </Flex>
    <Flex class="flex-column flex-sm-row">
      <v-textarea v-model="draft.lyrics" class="flex-grow-1" label="Lyrics" :rows="5" :max-rows="15" auto-grow></v-textarea>
      <Flex column>
        <v-textarea v-model="draft.comment" label="Comment" :rows="2" :max-rows="15" auto-grow></v-textarea>
        <span class="border pa-2" :style="{ 'max-width': br.isGreater('sm') ? '500px' : 'auto'}">{{ renderComment(session.url, draft) }}</span>
      </Flex>
    </Flex>

    <Flex column>
      <Json v-model="draft" v-model:previous="track" show-diff :copy="false" :paste="false" />
      <Flex>
        <v-btn prepend-icon="mdi-content-save" :disabled="!isChanged" variant="tonal" color="success" flat @click="save">Save</v-btn>
        <v-btn prepend-icon="mdi-restore" :disabled="!isChanged" variant="tonal" color="error" flat @click="reset">Reset</v-btn>
        <v-btn prepend-icon="mdi-download" :disabled="isChanged" type="submit">Download</v-btn>
      </Flex>
    </Flex>
  </v-form>
</template>