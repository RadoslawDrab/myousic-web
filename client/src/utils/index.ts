
export function download(fileName: string, blobOrUrl: string | Blob) {
    const link = document.createElement('a')
    link.href = typeof blobOrUrl === 'string' ? blobOrUrl : URL.createObjectURL(blobOrUrl)
    link.download = fileName
    link.click()
    URL.revokeObjectURL(link.href)
}

export function getTime(time: number, milliseconds: boolean = false) {
    const date = new Date(time)

    return date.getMinutes().toString().padStart(2, '0') + ':' + date.getSeconds().toString().padStart(2, '0') + (milliseconds ? ':' + date.getMilliseconds().toString().padStart(3, '0') : '')
}

/**
 * @returns Returns true if version is different than saved one
 */
export function checkVersion(): boolean {
    const name = `${import.meta.env.VITE_APP_NAME || 'APP'}_VERSION`
    const savedVersion = localStorage.getItem(name)
    const version = import.meta.env.VITE_VERSION
    if (savedVersion !== version) {
        localStorage.setItem(name, version)
        return true
    }
    return false
}