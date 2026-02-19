<script setup lang="ts">

import ExplicitnessIcon from '@/components/ExplicitnessIcon.vue'
import useApi from '@/composables/use-api'
import useData from '@/composables/use-data'
import { useDebounce } from '@/composables/use-debounce'
import { getTime } from '@/utils'
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
const propertyCellClass = 'px-0'
const valueCellClass = 'px-0 ps-2 ps-sm-5'

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
    { property: 'Track Time', value: getTime(item.value?.trackTimeMillis || 0) },
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

async function _getTrackData() {
  const data = await getTrackData(item.value)
  item.value.genres = data.genres
  item.value.lyrics = data.lyrics
  item.value.lyricsUrl = data.lyricsUrl
  item.value.genresUrl = data.genresUrl
}

onMounted(async () => {
  if (!item.value) {
    await router.replace('/')
    return
  }
  if (import.meta.env.PROD) await _getTrackData()

  if (!item.value.comment) {
    item.value.comment = local.value.defaultComment
  }
})

definePage({
  meta: {
    title: 'Track'
  }
})
</script>

<template>
  <v-card v-if="item" flat :loading="isLoading" :disabled="isLoading">
    <v-card-title class="border-b mb-3 d-flex align-center justify-space-between ga-1">
      <v-btn v-tooltip="'Get track data'" class="pa-1" icon="mdi-database-import" rounded="sm" flat @click="_getTrackData()"></v-btn>
      <v-btn class="px-0 px-md-2 text-none text-body-1 text-md-h6 " :href="session.url" target="_blank" variant="plain" flat>
        <span class="text-wrap">
          {{ item.artistName }} - {{ item.trackName }}
        </span>
      </v-btn>
    </v-card-title>
    <v-card-text class="d-flex flex-wrap flex-md-nowrap align-start justify-center ga-3 ga-sm-5">
      <ArtworkImage :small-render-size="500" :large-render-size="1000" :url="item.artworkUrl100" />
      <v-table class="flex-grow-1">
        <thead>
          <tr>
            <th :class="propertyCellClass">Property</th>
            <th :class="valueCellClass">Value</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="row in rows">
            <td :class="propertyCellClass">{{ row.property }}</td>
            <td :class="valueCellClass">
              <v-btn v-if="row.link" class="text-none px-0" variant="plain" target="_blank" :href="row.link" flat><span class="text-wrap">{{ row.value }}</span></v-btn>
              <component v-else-if="row.component" :is="row.component" v-bind="row.componentProps"></component>
              <v-chip v-else-if="row.chip" :color="typeof row.chip !== 'boolean' ? row.chip : 'secondary'">{{ row.value }}</v-chip>
              <span v-else>{{ row.value }}</span>
            </td>
          </tr>
          <tr>
            <td :class="propertyCellClass">
              <v-btn v-if="item.genresUrl" class="px-0 text-none" :href="item.genresUrl" variant="plain" target="_blank" flat>Genres</v-btn>
              <template v-else>Genres</template>
            </td>
            <td :class="valueCellClass">
              <v-combobox
                  v-model:model-value="item.genres"
                  class="py-2"
                  variant="solo-filled"
                  chips
                  closable-chips
                  multiple
                  hide-details
                  flat
              >
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
            <td :class="propertyCellClass">
              <v-btn v-if="item.lyricsUrl" class="px-0 text-none" :href="item.lyricsUrl" variant="plain" target="_blank" flat>Lyrics</v-btn>
              <template v-else>Lyrics</template>
            </td>
            <td :class="valueCellClass">
              <v-textarea
                  v-model="item.lyrics"
                  class="py-2"
                  variant="solo-filled"
                  :max-rows="15"
                  hide-details
                  auto-grow
              ></v-textarea>
            </td>
          </tr>
          <tr>
            <td :class="propertyCellClass">
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
            <td :class="valueCellClass">
              <v-textarea
                  v-model="itemComment"
                  class="py-2"
                  variant="solo-filled"
                  :rows="2"
                  placeholder="E.g. [URL: {{ url }}]"
                  persistent-placeholder
                  hide-details
                  auto-grow
              ></v-textarea>
              <div v-if="item.comment" class="border pa-2 text-gray-200" v-html="renderComment(session.url, item, {}, true)"></div>
            </td>
          </tr>
        </tbody>
      </v-table>
    </v-card-text>
    <v-card-actions class="flex-wrap justify-end border-t">
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
    <Json v-model="formattedItem" :paste="false" content-class="pa-2 pa-sm-4">
      <template #prependActions>
        <v-btn prepend-icon="mdi-format-columns" flat @click="stripJson = !stripJson">{{ stripJson ? 'Stripped' : 'Full' }}</v-btn>
      </template>
      <template #appendActions>
        <v-btn prepend-icon="mdi-close" flat @click="jsonDialog = false">Close</v-btn>
      </template>
    </Json>
  </v-dialog>
</template>