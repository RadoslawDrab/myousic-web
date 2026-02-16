import { defineStore } from 'pinia'

import { VAlert } from 'vuetify/components'

export type StatusType = 'info' | 'success' | 'warning' | 'error'

export type StatusHandlerProps = InstanceType<typeof VAlert>['$props']

export interface StatusHandlerData {
    type: StatusType
    props?: StatusHandlerProps
    title: string
    text?: string
    time?: number | false
    timestamp?: number | false
    closable?: boolean
}

const useStatus = defineStore('status', () => {
    const statuses = ref<StatusHandlerData[]>([])

    // @ts-expect-error Is complex type
    const data = computed<StatusHandlerData | null>(() => statuses.value.length > 0 ? statuses.value.at(0) : null)
    const hasStatus = computed(() => statuses.value.length > 0)
    function getStatusType(code: number): StatusType {
        if (code >= 200 && code < 300) {
            return 'success'
        } else if (code >= 300 && code < 400) {
            return 'warning'
        } else if (code >= 400) {
            return 'error'
        }
        return 'info'
    }
    function add(options: StatusHandlerData, time: number | false = false): void {
        // @ts-expect-error Doesn't contain proper keys now but will later
        let data: StatusHandlerData = {}
        if (options['code']) {
            const _options = options
            const entry = Object.entries(_options)
                                    .find(([key, value]) =>
                                        !['message', 't'].includes(key) && typeof value === 'string'
                                    )
            data = {
                type: _options.type,
                title: _options.title,
                text: entry ? entry[1] as string : undefined,
                closable: true,
                timestamp: _options.timestamp,
                time
            }

        } else {
            data = options as StatusHandlerData
        }
        statuses.value.push(data)
    }

    function removeFirst(beforeRemove?: (status: StatusHandlerData | null) => Promise<void>) {
        if (beforeRemove) {
            beforeRemove(data.value).then(() => statuses.value.shift())
            return
        }
        statuses.value.shift()
    }

    return { hasStatus, add, data, removeFirst, statuses }
})

export default useStatus