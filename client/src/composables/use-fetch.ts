import useStatus from '@/composables/use-status'
import { getApiUrl } from '@/utils/api'
import { deepMerge } from '@/utils/object'

type Options = {
    baseUrl?: string
    query?: Record<string, any>
    headers?: Record<string, any>
    path?: string | string[]
    responseType?: 'json' | 'blob'
}

const useFetch = (options: Options = { }) => {
    const status = ref<API_Response | null>(null)
    const isLoading = ref<boolean>(false)
    const st = useStatus()

    async function run<Resp>(body?: Record<string, any> | FormData | null, _options: Options = {}): Promise<Resp | null> {
        try {
            const method = this.toString().toUpperCase()
            isLoading.value = true

            const _opt = deepMerge(options, _options)
            const query = new URLSearchParams(_opt?.query || {})

            const url = getApiUrl(_opt?.baseUrl, ...(_opt?.path || [])) + '?' + query.toString()

            const isFormData = body && body instanceof FormData
            const contentType = isFormData ? 'multipart/form-data' : 'application/json'

            let _body: FormData = isFormData ? body : new FormData()
            if (body && !(body instanceof FormData)) _body.append('body', JSON.stringify(body))

            const response = await fetch(url, {
                method,
                headers: {
                    'Content-Type': contentType,
                    ..._opt?.headers
                },
                body: ['POST', 'PATCH', 'PUT'].includes(method) ? _body : undefined,
            })

            if (!response.ok) {
                const value = (await response.json()) || { code: response.status, message: response.statusText }
                st.add({ title: value.message, type: 'error' }, 5000)
                status.value = value
                return null
            }

            return await response[_opt.responseType || 'json']()
        } finally {
            isLoading.value = false
        }
    }

    return {
        status,
        isLoading,
        get: run.bind('GET'),
        post: run.bind('POST'),
        patch: run.bind('PATCH'),
        delete: run.bind('DELETE'),
        put: run.bind('PUT'),
    }
}

export default useFetch