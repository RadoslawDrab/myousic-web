When using iTunes download, the variables are fetched from the [iTunes API](https://performance-partners.apple.com/search-api).

Otherwise, variables are fetched from <span>YouTube</span> video metadata. Some may be empty.
<div style="font-size: 0.9rem">

| Name                    | Description               |                 Type                 | iTunes Download | Manual Download | Note                                                           |
|-------------------------|---------------------------|:------------------------------------:|:---------------:|:---------------:|----------------------------------------------------------------|
| `trackId`               | iTunes track id           |               `number`               |        ✔        |        ❌        |                                                                |
| `trackName`             | Track name                |               `string`               |        ✔        |        ✔        |                                                                |
| `trackCensoredName`     | Censored track name       |               `string`               |        ✔        |        ❌        |                                                                |
| `trackExplicitness`     | Track explicitness        |                   `explicit \| cleaned \| notExplicit`                   |        ✔        |        ❌         |                                                                |
| `trackNumber`           | Track number in album     |               `number`               |        ✔        |        ✔         |                                                                |
| `trackCount`            | Number of tracks in album |               `number`               |        ✔        |        ✔         |                                                                |
| `discNumber`            | Disc number               |               `number`               |        ✔        |        ✔         |                                                                |
| `discCount`             | Disc count                |               `number`               |        ✔        |        ✔         |                                                                |
| `trackTimeMillis`       | Track time in milliseconds |               `number`               |        ✔        |        ❌         |                                                                |
| `primaryGenreName`      | Main genre name           |               `string`               |        ✔        |        ✔         |                                                                |
| `releaseDate`           | ISO date string           |               `string`               |        ✔        |        ✔         |                                                                |
| `artworkUrl100`         | Artwork URL               |               `string`               |        ✔        |        ✔         | Manual Download: only set if the artwork file is not provided. |
| `trackViewUrl`          | iTunes track URL          |               `string`               |        ✔        |        ❌         |                                                                |
| `collectionId`          | iTunes album id           |               `number`               |        ✔        |        ❌        |                                                                |
| `collectionName`        | Album name                |               `string`               |        ✔        |        ✔        |                                                                |
| `collectionCensoredName` | Censored album name       |               `string`               |        ✔        |        ❌        |                                                                |
| `collectionExplicitness` | Album explicitness        | `explicit \| cleaned \| notExplicit` |        ✔        |        ❌         |                                                                |
| `collectionViewUrl`     | iTunes album URL          |               `string`               |        ✔        |        ❌         |                                                                |
| `artistId`              | iTunes artist id          |               `number`               |        ✔        |        ❌         |                                                                |
| `artistName`            | Artist name               |               `string`               |        ✔        |        ✔        |                                                                |
| `artistViewUrl`         | iTunes artist URL         |           `string \| null`           |        ✔        |        ❌         |                                                                |
| `lyrics`                | Track lyrics              |           `string \| null`           |        ✔        |        ✔        |                                                                |
| `lyricsUrl`             | Track lyrics url          |           `string \| null`           |        ✔        |        ✔        |                                                                |
| `genres`                | Track genres              |              `string[]`              |        ✔        |        ✔        |                                                                |
| `genresUrl`             | Track genres url          |           `string \| null`           |        ✔        |        ✔        |                                                                |

</div>
