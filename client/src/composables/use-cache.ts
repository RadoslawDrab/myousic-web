const useCache = (urlRef: Ref<string | null>, options?: { name?: string, init?: RequestInit, staleWhileRevalidate?: boolean }) => {
    const cacheName = import.meta.env.VITE_APP_NAME.toUpperCase().trim().replace(/\s/g, '_') + '_' + (options?.name || 'CACHE').toUpperCase().trim().replace(/\s/g, '_')
    const data = ref<string | null>(null)
    const isLoading = ref(false)
    const error = ref<any>(null)

    const execute = async (url: string) => {
        isLoading.value = true
        error.value = null

        try {
            const cache = await caches.open(cacheName)
            const cachedResponse = await cache.match(url)

            if (cachedResponse) {
                data.value = await cachedResponse.text()
                if (!options?.staleWhileRevalidate) return
            }

            // Background Network Fetch (Stale-While-Revalidate)
            const response = await fetch(url, options?.init)
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

    // Automatically trigger when the URL changes
    watch(urlRef, (newUrl) => {
        if (newUrl) execute(newUrl)
    }, { immediate: true })

    return {
        data,
        isLoading,
        error,
        refresh: () => urlRef.value && execute(urlRef.value)
    }
}

export default useCache