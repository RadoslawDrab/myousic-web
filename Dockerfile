FROM mwader/static-ffmpeg:6.1.1 AS ffmpeg-source

FROM node:20-alpine AS build-frontend
WORKDIR /frontend
COPY client/package*.json ./
RUN npm install --legacy-peer-deps
COPY client/ ./

ARG CLIENT_VERSION

ENV DEV=False
ENV CLIENT_APP_NAME=Myousic
ENV CLIENT_VERSION=$CLIENT_VERSION
ENV CLIENT_API_URL=/api

COPY .env* ./
RUN npm run build

FROM python:3.13-alpine AS build-backend
WORKDIR /app

# Copy static FFmpeg/FFprobe from Stage 1
COPY --from=ffmpeg-source /ffmpeg /usr/local/bin/
COPY --from=ffmpeg-source /ffprobe /usr/local/bin/

ARG DEV
ARG SERVER_LOG_LEVEL
ARG SERVER_AUDIO_AVAILABLE
ARG SERVER_ITUNES_URL

# Environment
ENV PYTHONUNBUFFERED=1
ENV	PYTHONDONTWRITEBYTECODE=1
ENV	LANG=C.UTF-8
ENV	LC_ALL=C.UTF-8

ENV DEV=False
ENV SERVER_LOG_LEVEL=$SERVER_LOG_LEVEL
ENV SERVER_AUDIO_AVAILABLE=$SERVER_AUDIO_AVAILABLE
ENV SERVER_ITUNES_URL=$SERVER_ITUNES_URL

# Python Requirements
COPY server/requirements.txt ./server/requirements.txt
RUN pip install --no-cache-dir -r server/requirements.txt

# Copy Frontend and Backend
COPY server/ ./server/
COPY --from=build-frontend /frontend/dist/ ./client

HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD python3 -c "import urllib.request; urllib.request.urlopen('http://localhost:80/').read()" || exit 1

EXPOSE 80

CMD python server/main.py \
 --prod \
 --port 80 \
 --host 0.0.0.0 \
 --log-path /app/log/myousic.log \
 --app-path /app/client \
 --output-path /app/audio
