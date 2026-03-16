
### 🚀 Welcome to the Myousic - Simplified music downloader

This application provides a seamless way to download audio from YouTube videos, 
elevating your experience with rich, accurate metadata from the iTunes catalog. 
Forget generic file names and missing album art – this tool integrates advanced 
processing to deliver high-quality audio files.


### ✨ Key Features

- **Intelligent Metadata Matching**: Uses the YouTube video title to search the iTunes API for official song, artist, and album information.
- **Automatic Tagging & Artwork**: Downloads high-resolution album art and embeds comprehensive ID3 tags (artist, album, track number, year) directly into your audio file.
- **Customizable Audio Output**: Choose your preferred file format (M4A, MP3, FLAC, WAV, Opus) and adjust audio quality settings like sample rate.
- **Advanced Lyrics Integration**: Fetches lyrics from multiple providers with a configurable priority order and an optional profanity filter.
- **Flexible Content Filtering**: Exclude or unwanted genres from search results to ensure you only get relevant music tracks.

### 🛠️ Technical Prerequisite

This application relies heavily on [FFmpeg](https://ffmpeg.org/) for all audio extraction, conversion, and metadata embedding tasks. 
FFmpeg **must be** installed on the server hosting this application and accessible via the system's _PATH_. 
Without FFmpeg, audio processing will fail.