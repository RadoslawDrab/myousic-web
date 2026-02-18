
export function download(fileName: string, blob_or_url: string | Blob) {
    const link = document.createElement('a')
    link.href = typeof blob_or_url === 'string' ? blob_or_url : URL.createObjectURL(blob_or_url)
    link.download = fileName
    link.click()
    URL.revokeObjectURL(link.href)
}

export function getTime(time: number) {
    const date = new Date(time)

    return date.getMinutes().toString().padStart(2, '0') + ':' + date.getSeconds().toString().padStart(2, '0')
}