The settings panel allows you to define the behavior of the downloader, metadata matching, and file conversion.
Settings can be imported and exported as `JSON`.

_These configurations are applied globally._

### Lyrics

| Field | Description                                                                                                                                     |
| --- |-------------------------------------------------------------------------------------------------------------------------------------------------|
| Lyrics Provider Order | Defines the order of the lyrics providers to use.                                                                                               |
| Lyrics Modifier | Defines the modifier to use for the lyrics. This is used to modify the lyrics before embedding them into the file. Keys allow usage of _Regex_. |

### Genres

| Field | Description                                                               |
| --- |---------------------------------------------------------------------------|
| Included Genres | Defines the genres to include in the metadata. Allows usage of _Regex_.   |
| Excluded Genres | Defines the genres to exclude from the metadata. Allows usage of _Regex_. |

### General

| Field | Description                                                                                                                                                                                                                         |
| --- |-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Artwork Size | Defines artwork size in pixels. The artwork will be scaled to this size. **Used only when fetched from iTunes.**                                                                                                                    |
| Extension | Defines the file extension of the output file.                                                                                                                                                                                      |
| Sample Rate | Defines the sample rate of the output file. Changes based on extension type to accommodate the format.                                                                                                                              |
| Default Comment | Defines the default comment to use. Each comment can be changed per file. Allows [variables](/docs/settings/variables) to be used. For more info check [mustache](https://github.com/janl/mustache.js?tab=readme-ov-file#variables) |


## Storage

App data is stored on user browser. 
List of storages and their purposes:

| Name               | Storage          | Purpose                                                                |
|--------------------|------------------|------------------------------------------------------------------------|
| `MYOUSIC_SETTINGS` | `localStorage`   | Stores user's settings to keep them between sessions.                  |
| `MYOUSIC_DATA`     | `sessionStorage` | Stores user's url, last search result and other session data.          |
| `MYOUSIC_DOCS`     | `sessionStorage` | Stores docs data from `docs.json`.                                     |
| `MYOUSIC_TRACK`    | `sessionStorage` | Stores data of manual download track. Artwork file is not saved.       |
| `MYOUSIC_CACHE`    | `cacheStorage`   | Stores data like social icons and docs which are not updated regularly |