<script setup lang="ts">

import ExplicitnessIcon from '@/components/ExplicitnessIcon.vue'
import useApi from '@/composables/use-api'
import useData from '@/composables/use-data'
import { useDebounce } from '@/composables/use-debounce'
import { getArtworkUrl } from '@/utils/api'
import { pascalCase } from '@/utils/string'

const route = useRoute()
const router = useRouter()
const { downloadTrack, getTrackData, renderComment, isLoading } = useApi()
const { session, local } = useData()


const props = withDefaults(defineProps<{
  jsonKeys?: (keyof SearchAPI_TrackResult)[]
}>(), {
  jsonKeys: () => ['artistName', 'collectionName', 'collectionCensoredName', 'trackName', 'trackCensoredName', 'primaryGenreName', 'trackExplicitness', 'collectionExplicitness', 'trackNumber', 'trackCount', 'discNumber', 'discCount', 'trackTimeMillis', 'releaseDate', 'artworkUrl100']
})

const item = computed<(SearchAPI_TrackResult & ExtendedTrack) | null>(() => ((session.value.items || []) as SearchAPI_TrackResult[]).find(track => track.trackId == route.params.item) || null)

const jsonDialog = ref<boolean>(false)
const censored = ref<boolean>(true)
const stripJson = ref<boolean>(true)
const lyricsUrl = ref<string>('')
const genresUrl = ref<string>('')

const itemComment = useDebounce(item, 1500, { targetKey: 'comment' })

const rows = computed<{ property: string, value: any, link?: string, component?: Component, componentProps?: Record<string, any>, chip?: boolean | string }[]>(() => {
  return item.value ? [
    { property: 'Artist', value: item.value?.artistName, link: item.value?.artistViewUrl },
    { property: 'Album', value: censored.value ? item.value?.collectionCensoredName : item.value?.collectionName, link: item.value?.collectionViewUrl },
    { property: 'Track', value: censored.value ? item.value?.trackCensoredName : item.value?.trackName, link: item.value?.trackViewUrl },
    { property: 'Genre', value: item.value?.primaryGenreName, chip: 'primary' },
    { property: 'Track Explicitness', value: item.value?.trackExplicitness, component: ExplicitnessIcon, componentProps: { value: item.value?.trackExplicitness } },
    { property: 'Collection Explicitness', value: item.value?.collectionExplicitness, component: ExplicitnessIcon, componentProps: { value: item.value.collectionExplicitness } },
    { property: 'Track Number', value: `${item.value?.trackNumber} / ${item.value?.trackCount}`},
    { property: 'Disc Number', value: `${item.value?.discNumber} / ${item.value?.discCount}`},
    { property: 'Track Time', value: new Date(item.value?.trackTimeMillis).toLocaleTimeString() },
    { property: 'Release Date', value: new Date(item.value?.releaseDate).toLocaleDateString() },

  ] : []
})

const formattedItem = computed(() => {
  if (!stripJson.value) return item.value

  const obj =  props.jsonKeys.reduce((acc, key) => {
    acc[key] = item.value[key]
    return acc
  }, {})

  if (item.value.artworkUrl100 && props.jsonKeys.includes('artworkUrl100')) obj['artworkUrl1000'] = getArtworkUrl(item.value.artworkUrl100)
  return obj
})

const itemGenres = computed({
  get() {
    return (item.value?.genres || [])
  },
  set(value) {
    item.value.genres = value.map(v => pascalCase(v))
  }
})

async function _getTrackData() {
  const data = await getTrackData(item.value, local.value)
  item.value.genres = data.genres
  item.value.lyrics = data.lyrics
  lyricsUrl.value = data.lyricsUrl
  genresUrl.value = data.genresUrl

}

onMounted(async () => {
  if (!item.value) {
    await router.replace('/')
    return
  }
  // if (item.value.genres)
  await _getTrackData()
})
</script>

<template>
  <UrlDataSearch class="mb-3 flex-grow-1" />
  <v-card v-if="item" flat :loading="isLoading" :disabled="isLoading">
    <v-card-title class="border-b mb-3 d-flex align-center justify-space-between ga-2">
      <Flex :gap="2">
        <v-btn v-tooltip="'Refresh'" class="pa-1" icon="mdi-restore" rounded="sm" flat @click="_getTrackData()"></v-btn>
      </Flex>
      {{ item.artistName }} - {{ item.trackName }}
    </v-card-title>
    <v-card-text class="d-flex align-start ga-3">
      <ArtworkImage :small-render-size="500" :large-render-size="1000" :url="item.artworkUrl100" />
      <v-table class="flex-grow-1">
        <thead>
          <tr>
            <th>Property</th>
            <th>Value</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="row in rows">
            <td>{{ row.property }}</td>
            <td>
              <v-btn v-if="row.link" class="text-none px-0" variant="plain" target="_blank" :href="row.link" flat>{{ row.value }}</v-btn>
              <component v-else-if="row.component" :is="row.component" v-bind="row.componentProps"></component>
              <v-chip v-else-if="row.chip" :color="typeof row.chip !== 'boolean' ? row.chip : 'secondary'">{{ row.value }}</v-chip>
              <span v-else>{{ row.value }}</span>
            </td>
          </tr>
          <tr>
            <td>
              <v-btn class="px-0 text-none" :href="genresUrl" variant="plain" target="_blank" flat>Genres</v-btn>
            </td>
            <td class="py-2">
              <v-combobox v-model:model-value="item.genres" :items="item.genres" chips multiple>
                <template #chip="{ item, props: internalProps }">
                  <v-chip v-bind="internalProps">{{ pascalCase(item.value) }}</v-chip>
                </template>
                <template #item="{ item: internalItem, props: internalProps }">
                  <v-list-item :title="pascalCase(internalItem.value)" variant="plain" v-bind="internalProps">
                  </v-list-item>
                </template>
              </v-combobox>
            </td>
          </tr>
          <tr>
            <td>
              <v-btn class="px-0 text-none" :href="lyricsUrl" variant="plain" target="_blank" flat>Lyrics</v-btn>
            </td>
            <td class="py-2">
              <v-textarea
                  v-model="item.lyrics"
                  variant="solo-filled"
                  :max-rows="15"
                  auto-grow
              ></v-textarea>
            </td>
          </tr>
          <tr>
            <td>
              <p>Comment</p>
              <v-btn
                  class="text-caption text-none pa-0"
                  to="/docs/comment"
                  variant="plain"
                  target="_blank"
                  density="compact">
                See docs
              </v-btn>
            </td>
            <td class="py-2">
              <v-textarea
                  v-model="itemComment"
                  variant="solo-filled"
                  :rows="2"
                  hint="Testing"
                  placeholder="E.g. [URL: $url$]"
                  persistent-placeholder
                  auto-grow
              ></v-textarea>
              <div v-if="item.comment" class="border pa-2 text-gray-200" v-html="renderComment(session.url, item, {}, true)"></div>
            </td>
          </tr>
        </tbody>
      </v-table>
    </v-card-text>
    <v-card-actions>
      <v-btn :prepend-icon="censored ? 'mdi-eye' : 'mdi-eye-off'" variant="text" flat @click="censored = !censored">
        {{ censored ? 'Censored' : 'Uncensored' }}
      </v-btn>
      <v-btn prepend-icon="mdi-play" flat target="_blank" :href="item.previewUrl">Preview</v-btn>
      <v-btn prepend-icon="mdi-download" :disabled="!session.url" flat @click="downloadTrack(session.url, item)">
        Download
      </v-btn>
      <v-btn prepend-icon="mdi-code-json" flat @click="jsonDialog = true">View JSON</v-btn>
    </v-card-actions>
  </v-card>
  <span v-else>Not found</span>

  <v-dialog v-model="jsonDialog" max-width="700px">
    <Json v-model="formattedItem" :paste="false">
      <template #prependActions>
        <v-btn prepend-icon="mdi-format-columns" flat @click="stripJson = !stripJson">{{ stripJson ? 'Stripped' : 'Full' }}</v-btn>
      </template>
      <template #appendActions>
        <v-btn prepend-icon="mdi-close" flat @click="jsonDialog = false">Close</v-btn>
      </template>
    </Json>
  </v-dialog>
</template>