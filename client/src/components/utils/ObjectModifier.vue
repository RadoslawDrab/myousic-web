<script setup lang="ts" generic="T extends Record<any, any> | any[]">
import { joinClass } from '@/utils/string'
import { SubmitEventPromise } from 'vuetify/framework'

type Rule = (value: string) => string | boolean

const object = defineModel<T>()

const props = defineProps<{
  valueType?: 'string' | 'number' | 'boolean'
  keyPlaceholder?: string
  valuePlaceholder?: string
  keyHint?: string
  valueHint?: string
  keyLabel?: string
  valueLabel?: string
}>()

const items = ref<[keyof T, string | number | boolean][]>(Object.entries(object.value))

const isArray = computed(() => Array.isArray(object.value))

const rules = computed<{ key: (index: number) => Rule[], value: (index: number) => Rule[] }>(() => {
  return {
    key: (index: number) => [
      (value: string) => {
        if (!value) return 'Key is required'
        if (items.value.some(([key], i) => key === value && i !== index)) return 'Key already exists'
        return true
      }
    ],
    value: (index: number) => [
      (value: string) => {
        return true
      }
    ]
  }
})

function reset() {
  items.value = Object.entries(object.value)
}

async function save(event: SubmitEventPromise) {
  const check = await event
  if (!check.valid) return

  object.value = isArray.value ?
      items.value.map(([key, value]) => value) :
      items.value.reduce((acc, [key, value]) => {
        acc[key] = value
        return acc
      }, {} as T)
}

</script>

<template>
  <v-form @submit.prevent="save" validate-on="blur lazy">
    <v-list class="py-0 bg-transparent" density="compact">
      <v-list-item v-for="(_, index) in items" class="py-3" :class="joinClass(index > 0 && 'border-t pt-3')" :key="index">
        <Flex :gap="2">
          <v-btn
              class="pa-1"
              icon="mdi-minus"
              rounded="sm"
              flat
              @click="items = items.filter((_, i) => i !== index)"
          >
          </v-btn>
          <v-text-field
              v-if="!isArray"
              v-model="items[index][0]"
              variant="solo-filled"
              :rules="rules.key(index)"
              :placeholder="props.keyPlaceholder"
              :hint="props.keyHint"
              :label="props.keyLabel || 'Key'"
              :persistent-placeholder="!!props.keyPlaceholder"
              :persistent-hint="!!props.keyHint"
          >
          </v-text-field>

          <slot
              :item="items[index]"
              :index="index"
              :rules="rules.value(index)"
          >
            <v-text-field
                v-if="!props.valueType || props.valueType === 'string'"
                v-model="items[index][1]"
                variant="solo-filled"
                :rules="rules.value(index)"
                :placeholder="props.valuePlaceholder"
                :hint="props.valueHint"
                :label="props.valueLabel || 'Value'"
                :persistent-placeholder="!!props.valuePlaceholder"
                :persistent-hint="!!props.valueHint"
            >
            </v-text-field>
            <v-number-input
                v-else-if="props.valueType === 'number'"
                v-model="items[index][1] as number"
                variant="solo-filled"
                :rules="rules.value(index)"
                :placeholder="props.valuePlaceholder"
                :hint="props.valueHint"
                :label="props.valueLabel || 'Value'"
                :persistent-placeholder="!!props.valuePlaceholder"
                :persistent-hint="!!props.valueHint"
            >
            </v-number-input>
            <v-switch
                v-else-if="props.valueType === 'boolean'"
                v-model="items[index][1]"
                variant="solo-filled"
                :placeholder="props.valuePlaceholder"
                :hint="props.valueHint"
                :label="props.valueLabel || 'Value'"
                :persistent-placeholder="!!props.valuePlaceholder"
                :persistent-hint="!!props.valueHint"
            >
            </v-switch>
          </slot>
        </Flex>
      </v-list-item>
      <v-list-item class="pa-2" :class="joinClass(items.length > 0 && 'border-t')">
        <Flex :gap="2">
          <v-btn
              prepend-icon="mdi-plus"
              flat
              @click="items.push([isArray ? items.length : '', '', 'string'])"
          >
            Add
          </v-btn>
          <v-btn
              type="submit"
              prepend-icon="mdi-content-save"
              flat
          >
            Save
          </v-btn>
          <v-btn
              prepend-icon="mdi-restore"
              flat
              @click="reset"
          >
            Reset
          </v-btn>
        </Flex>
      </v-list-item>
    </v-list>
  </v-form>
</template>