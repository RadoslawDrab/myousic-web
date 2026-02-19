<script setup lang="ts">
import useApi from '@/composables/use-api'
import useData from '@/composables/use-data'
import { getTime } from '@/utils'

const { searchApi, downloadTrack, getTrackData, renderComment, isLoading } = useApi()

const { session } = useData()

const items = ref<SearchAPI_Result[]>(session.value.items || [])

const headerFilter = useTemplateRef('headerFilter')
const allHeaders = ref<DataTableHeader[]>([])
const headers = ref(allHeaders.value)

const urlKeys = computed<[keyof SearchAPI_ResultKeys, keyof SearchAPI_ResultKeys][]>(() => {
  switch (session.value.entity) {
    case 'album':
      return [
        ['collectionName', 'collectionViewUrl'],
        ['collectionCensoredName', 'collectionViewUrl'],
        ['artistName', 'artistViewUrl'],
      ]
    case 'musicArtist':
      return [
        ['artistName', 'artistViewUrl'],
      ]
    default:
      return [
        ['trackName', 'trackViewUrl'],
        ['trackCensoredName', 'trackViewUrl'],
        ['artistName', 'artistViewUrl'],
        ['collectionName', 'collectionViewUrl'],
        ['collectionCensoredName', 'collectionViewUrl'],
        ['artistName', 'artistLinkUrl'],
      ]
  }
})

const explicitKeys: (keyof SearchAPI_ResultKeys)[] = ['collectionExplicitness', 'trackExplicitness']

async function onDownload(item: SearchAPI_Result) {
  const _item = { ...item } as ExtendedTrack
  const {lyrics, genres} = await getTrackData(_item)
  _item.lyrics = lyrics
  _item.comment = renderComment(session.value.url, _item, { genres, lyrics })

  await downloadTrack(session.value.url, _item)
}

watch([() => session.value.search, () => session.value.entity], async ([search, entity]) => {
  if (!search) {
    items.value = []
    return
  }

  const { results } = await searchApi({ term: search, entity: entity as SearchAPI_Entity })
  items.value = results
})

watch(() => session.value.entity, (entity) => {
  let headers: DataTableHeader[] = []
  const albumHeaders: DataTableHeader[] = [
    { title: 'Album Name', key: 'collectionName' },
    { title: 'Album Censored Name', key: 'collectionCensoredName', defaultShow: false },
    { title: 'Album Explicitness', key: 'collectionExplicitness', defaultShow: false },
  ]
  switch (entity) {
    case 'album':
      headers = [
        { title: 'Artist Name', key: 'artistName' },
        { title: 'Artwork', key: 'artworkUrl100' },
        ...albumHeaders
      ]
      break
    case 'musicArtist':
      headers = [
        { title: 'Artist Name', key: 'artistName' },
        { title: 'Artist Type', key: 'artistType', defaultShow: false },
        { title: 'Primary Genre', key: 'primaryGenreName' },
      ]
      break
    default:
      headers = [
        { title: 'Actions', key: 'actions', removable: false, sortable: false },
        { title: 'Artwork', key: 'artworkUrl100' },
        { title: 'Track Name', key: 'trackName' },
        { title: 'Track Censored Name', key: 'trackCensoredName', defaultShow: false },
        { title: 'Track Explicitness', key: 'trackExplicitness', defaultShow: false },
        { title: 'Track Data', key: 'trackData', defaultShow: false },
        { title: 'Disc Data', key: 'discData', defaultShow: false },
        { title: 'Track Time', key: 'trackTimeMillis', defaultShow: false },
        { title: 'Track Genre', key: 'primaryGenreName', defaultShow: false },
        { title: 'Artist Name', key: 'artistName' },
        ...albumHeaders,
      ]
      break
  }
  allHeaders.value = headers
  nextTick(() => headerFilter.value && headerFilter.value.init())
}, { immediate: true })

watch(items, (items) => {
  session.value.items = items
}, { deep: true, immediate: true })

definePage({
  meta: {
    title: 'Home'
  }
})
</script>

<template>
  <UrlDataSearch class="mb-3 flex-grow-1" />
  <SearchBar>
    <HeadersFilter ref="headerFilter" v-model="headers" v-model:all-headers="allHeaders"  />
  </SearchBar>
  <v-divider class="my-4" />
  <v-data-table
      :headers="headers"
      :loading="isLoading"
      :items="items"
  >
    <template #item.actions="{ item }">
      <v-btn-group density="compact">
        <v-btn icon="mdi-download" :disabled="!session.url" flat @click="onDownload(item)"></v-btn>
        <v-btn icon="mdi-eye" flat :to="`/${item.wrapperType}/${item.trackId || item.collectionId || item.artistId}`"></v-btn>
      </v-btn-group>
    </template>
    <template
        v-for="key in urlKeys"
        #[`item.${String(key[0])}`]="{ value, item}">
      <v-btn v-if="value" class="text-none px-0" :href="item[key[1]]" variant="plain" target="_blank" flat>{{ value.trim() }}</v-btn>
      <span v-else>-</span>
    </template>
    <template
        v-for="key in explicitKeys"
        #[`item.${String(key)}`]="{ value, item }"
    >
      <ExplicitnessIcon :value="value" />
    </template>
    <template #item.artworkUrl100="{ value }">
      <ArtworkImage :url="value" />
    </template>
    <template #item.trackTimeMillis="{ value }">
      {{ getTime(value) }}
    </template>
    <template #item.primaryGenreName="{ value }">
      <v-chip base-color="primary">{{ value }}</v-chip>
    </template>
    <template #item.trackData="{ item }">
      {{ item.trackNumber }} / {{ item.trackCount }}
    </template>
    <template #item.discData="{ item }">
      {{ item.discNumber }} / {{ item.discCount }}
    </template>
  </v-data-table>
</template>
