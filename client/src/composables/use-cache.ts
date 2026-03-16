const useCache = (urlRef: Ref<string | null>, options?: { name?: string, init?: RequestInit, staleWhileRevalidate?: boolean }) => {
    const cacheName = (import.meta.env.VITE_APP_NAME || 'APP').toUpperCase().trim().replace(/\s/g, '_') + '_' + (options?.name || 'CACHE').toUpperCase().trim().replace(/\s/g, '_')
    const data = ref<string | null>(null)
    const isLoading = ref(false)
    const error = ref<any>(null)

    const execute = async (url: string, fetchOptions?: RequestInit, force: boolean = false) => {
        isLoading.value = true
        error.value = null

        try {
            const cache = await caches.open(cacheName)
            const cachedResponse = await cache.match(url)

            if (cachedResponse && !force) {
                data.value = await cachedResponse.text()
                if (options?.staleWhileRevalidate ?? true) return
            }

            // Background Network Fetch (Stale-While-Revalidate)
            const response = await fetch(url, fetchOptions || options?.init)
            if (response.ok) {
                const text = await response.clone().text()

                // Update cache for next time
                await cache.put(url, response)

                // Update ref if content changed
                if (text !== data.value) {
                    data.value = text
                }
            }
        } catch (err) {
            error.value = err
            console.error('Cache fetch error:', err)
            data.value = null
        } finally {
            isLoading.value = false
        }
    }

    async function getCache(callback: (text: string, request: Request) => boolean, loopAll: boolean = false) {
        const cache = await caches.open(cacheName)


        for (const req of await cache.keys()) {
            const resp = await fetch(req.url)

            if (!resp.ok) continue

            if (callback(await resp.text(), req) && !loopAll) return
        }
    }

    // Automatically trigger when the URL changes
    watch(urlRef, (urlData) => {
        if (!urlData) return
        execute(urlData)
    }, { immediate: true })

    return {
        data,
        isLoading,
        error,
        getCache,
        refresh: (init?: RequestInit, force: boolean = true) => urlRef.value && execute(urlRef.value, init, force)
    }
}

export type CacheReturn = ReturnType<typeof useCache>
export default useCache