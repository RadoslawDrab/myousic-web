<script setup lang="ts">
import { joinClass } from '@/utils/string'
import { VListItem, VListGroup, VListItemTitle } from 'vuetify/components'

const props = withDefaults(defineProps<{
  itemKey?: string
  icon?: string,
  title?: string
  tooltip?: string | boolean
  class?: string | string[]
  itemClass?: string | string[]
  titleClass?: string | string[]
  groupClass?: string | string[]
  groupItemClass?: string | string[]
  groupContentClass?: string | string[]
  props?: InstanceType<typeof VListItem>['$props']
  titleProps?: InstanceType<typeof VListItemTitle>['$props']
  groupProps?: InstanceType<typeof VListGroup>['$props']
  groupCondition?: 'slot' | (() => boolean)
}>(), {
  tooltip: false
})

function getClass(value: string | string[]): string[] {
  return Array.isArray(value) ? value : [value]
}
const classes = computed(() => getClass(props.class))
const itemClasses = computed(() => getClass(props.itemClass))
const titleClasses = computed(() => getClass(props.titleClass))
const groupClasses = computed(() => getClass(props.groupClass))
const groupItemClasses = computed(() => getClass(props.groupItemClass))
const groupContentClasses = computed(() => getClass(props.groupContentClass))

const condition = props.groupCondition && typeof props.groupCondition === 'function' ? props.groupCondition() : null

</script>

<template>
  <v-list-item
      v-if="condition || !$slots.group"
      v-tooltip="props.tooltip !== false ? props.tooltip !== true ? props.tooltip : props.title : ''"
      :class="joinClass(...classes, ...itemClasses)"
      :prepend-icon="props.icon"
      slim
      v-bind="props.props"
  >
    <slot name="text">
      <v-list-item-title :class="joinClass('mb-2', ...titleClasses)" v-bind="props.titleProps">{{ props.title }}</v-list-item-title>
    </slot>
    <slot></slot>
  </v-list-item>
  <v-list-group
      v-else
      :class="joinClass(...classes, ...groupClasses)"
      :value="props.itemKey || props.title"
      v-bind="props.groupProps"
  >
    <template v-slot:activator="{ props: internalProps }">
      <v-list-item
          v-tooltip="props.tooltip !== false ? props.tooltip !== true ? props.tooltip : props.title : ''"
          :class="joinClass(...classes, ...groupItemClasses)"
          slim
          v-bind="internalProps"
          :prepend-icon="props.icon"
      >
        <slot name="text">
          {{ props.title }}
        </slot>
      </v-list-item>
    </template>
    <div :class="joinClass(...classes, ...groupContentClasses)">
      <slot name="group"></slot>
    </div>
  </v-list-group>
</template>



<!--<script setup lang="ts">-->
<!--import { VListItem, VListItemTitle } from 'vuetify/components'-->

<!--  const props = defineProps<{-->
<!--    title?: string-->
<!--    titleProps?: InstanceType<typeof VListItemTitle>['$props']-->
<!--    itemProps?: InstanceType<typeof VListItem>['$props']-->
<!--  }>()-->
<!--</script>-->

<!--<template>-->
<!--  <v-list-item v-if="!$slots.group" v-bind="props.itemProps">-->
<!--    <slot name="text">{{ props.title }}</slot>-->
<!--    <slot></slot>-->
<!--    test-->
<!--  </v-list-item>-->
<!--  <v-list-group v-else>-->
<!--    <template #activator="{ props: internalProps }">-->
<!--      <v-list-item v-bind="internalProps">-->
<!--        <slot name="text" :title="props.title">-->
<!--          <v-list-item-title v-bind="props.titleProps">{{ props.title }}</v-list-item-title>-->
<!--        </slot>-->
<!--      </v-list-item>-->
<!--      <slot name="group"></slot>-->
<!--      other-->
<!--    </template>-->
<!--  </v-list-group>-->
<!--</template>-->