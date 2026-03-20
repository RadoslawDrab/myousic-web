# 🎵 Myousic

A web-based tool to download YouTube audio with iTunes metadata matching.
Features automatic exif data, artwork embedding, and both lyrics and genres retrieval.

## ✨ Features

- 🌐 **Source:** YouTube (via `yt-dlp`)
- 🏷️ **Metadata:** iTunes API matching
- 🎧 **Audio Processing:**
  - 🔄 Format conversion (MP3, M4A, FLAC, WAV, Opus)
  - 📈 Sample rate up to 192kHz
  - 🔊 Audio clipping
- 📝 **Lyrics:** Multi-provider support with customizable profanity filtering
- ⚙️ **Customization:** Genre inclusion and exclusion, artwork resizing, variable comment injection

## 🛠️ Tech Stack

- 🎨 **Frontend**: [Vue 3 (Composition API)](https://vuejs.org/), [Vuetify 3](https://vuetifyjs.com/en/), [Vue Router](https://router.vuejs.org/)
- 🐍 **Backend**: Python wrapper for [yt-dlp](https://github.com/yt-dlp/yt-dlp). Uses Flask as API server.

## 📚 Documentation

Detailed guides are available in the client/public/docs directory available in build.
Covers:

- 🛤️ Workflow logic
- 🌍 Global settings
- 🗺️ App navigation

## 💾 Installation

### 1. 🐳 Docker

```bash
docker run -d \
  --name myousic \
  -p 5000:80 \
  -v ./data:/app/audio \
  -v ./logs:/var/log \
  --restart unless-stopped \
  radziogadzio/myousic:latest
```

### 2. 🏗️ Docker Compose

```yaml
services:
  myousic:
    image: radziogadzio/myousic:latest
    container_name: myousic
    ports:
      - '8080:80'
    volumes:
      # Path to generated audio
      - ./audio:/app/audio
      - ./logs:/var/log
    restart: unless-stopped
```
