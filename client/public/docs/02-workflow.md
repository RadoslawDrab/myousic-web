## ➡️ Your Audio Download Workflow

Understanding the workflow is key to getting the best results. Our application bridges the gap between <span>YouTube's</span> vast video library and <span>iTunes'</span> rich music metadata, giving you perfectly tagged and formatted audio files.

### 🚶 Step-by-Step Guide

1. **Configure**: Before searching, customize your preferences in the settings page. You can choose the output file extension, sample rate, artwork size, and lyrics options. Settings are saved in browser and can be exported to _JSON_
2. **Paste YouTube URL**: Begin search by pasting any valid YouTube video link into the URL input field.
3. **Automatic Title Retrieval**: The application extracts the video title from YouTube. This title is then used as the primary query for the iTunes API.
4. **iTunes Metadata Search**: The system performs a smart search against the iTunes catalog to find matching songs or albums. It prioritizes official releases to ensure accuracy.
5. **Select Best Match**: You will be presented with a list of potential matches from iTunes. It is crucial to select the correct entry that corresponds to your desired song. This selection dictates the album art, artist, album name, genre, and track number that will be embedded into your final audio file.
6. **Configure metadata**: Fetch and embed lyrics, genres and comment.  
7. **Download & Process**: Once configured, click the "Download" button. The application will:
   - Extract the highest quality audio stream from the YouTube video.
   - Convert it to your selected format and sample rate (using FFmpeg).
   - Embed the chosen iTunes metadata (album art, tags).
   - Deliver your perfectly prepared audio file.


### Graph

```mermaid
graph TD
    
    %% CLIENT SIDE
    CA([User pastes YouTube URL])
    CB[Retrieve YouTube title]
    CC[Search iTunes API]
    CD{Present iTunes matches to user}
    CD1A{User selects match}
    CD1B[Show iTunes track info]
    CD2A([Manual download])
    CD2B[Show editable YouTube track info]
    
    %% SERVER SIDE    
    SA[Download YouTube file]
    SB[Apply audio filters and extracts using FFmpeg]
    SC[Download artwork from URL/file]
    SD[Embed metadata and artwork]
    SE[Save file on server]
    SF[Deliver file to client]
    
    UserEdit([User edits allowed data])
    FetchContent[\Fetch lyrics and genres/]
    ContentFilter[Apply content filters if set]
    Download[/Download track/]
    
    subgraph ClientSide [Client Side]
       CA --> CB --> CC --> CD
       
       CD -- Match is found --> CD1A
       CD -- Match is not found --> CD2A
       
       CD1A -- View --> CD1B --> FetchContent
       CD1A -- "Download <br /> (Uses default settings)" --> FetchContent 
       
       CD2A --> CD2B --> FetchContent --> ContentFilter --> Download
       
       ContentFilter <-- Not applicable if quick download --> UserEdit
    end
    
    subgraph ServerSide [Server Side]
       Download --> SA --> SB --> SC --> SD --> SE --> SF
       SBG[(Clean up files once per week)]
       
    
    end
```