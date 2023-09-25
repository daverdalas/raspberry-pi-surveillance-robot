<script setup lang="ts">
import { WebRTCPlayer } from '@eyevinn/webrtc-player'
import { nextTick, ref } from 'vue'
import { socket } from '@/socket'

const video = ref<HTMLVideoElement | null>(null)
const started = ref(false)
const playing = ref(true)
const videoCover = ref(false)

async function startStream(): Promise<void> {
  started.value = true
  socket.emit('stream', { action: 'start' })
  await nextTick()
  const player = new WebRTCPlayer({
    video: video.value as HTMLVideoElement,
    type: 'whep'
  })
  await player.load(new URL(import.meta.env.VITE_STREAM_URL as string))
}

function togglePlay(): void {
  playing.value = !playing.value
  if (playing.value) {
    video.value?.play()

    return
  }

  video.value?.pause()
}
</script>

<template>
  <button class="start-button" type="button" v-if="!started" @click="startStream">Start</button>
  <div v-else class="stream-container">
    <video
      class="stream-container__video"
      :class="{ 'stream-container__video--cover': videoCover }"
      ref="video"
      autoplay
      muted
      playsinline
    />
    <div class="stream-container__controls">
      <div class="stream-container__control" @click="videoCover = !videoCover">
        <font-awesome-icon v-if="videoCover" :icon="['fas', 'compress']" />
        <font-awesome-icon v-else :icon="['fas', 'expand']" />
      </div>
      <div class="stream-container__control" @click="togglePlay">
        <font-awesome-icon v-if="playing" :icon="['fas', 'pause']" />
        <font-awesome-icon v-else :icon="['fas', 'play']" />
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
button.start-button {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  cursor: pointer;
  outline: 0;
  text-transform: uppercase;
  color: #fff;
  background-color: #0d6efd;
  display: inline-block;
  font-weight: bold;
  line-height: 1.5;
  text-align: center;
  border: 1px solid transparent;
  padding: 8px 14px;
  font-size: 1.4rem;
  border-radius: 0.25rem;
  transition:
    color 0.15s ease-in-out,
    background-color 0.15s ease-in-out,
    border-color 0.15s ease-in-out,
    box-shadow 0.15s ease-in-out;

  :hover {
    color: #fff;
    background-color: #0b5ed7;
    border-color: #0a58ca;
  }
}

.stream-container {
  position: relative;
  width: 100vw;
  height: 100vh;

  &__video {
    width: 100%;
    height: 100%;
    position: absolute;
    left: 0;
    top: 0;

    &--cover {
      object-fit: cover;
    }
  }

  &__controls {
    display: flex;
    position: absolute;
    bottom: 0;
    right: 0;
    background: rgba(255, 255, 255, 0.1);
  }

  &__control {
    cursor: pointer;
    padding: 5px;

    svg {
      display: block;
      width: 30px;
      height: 30px;
    }
  }
}
</style>
