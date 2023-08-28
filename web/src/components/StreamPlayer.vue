<script setup lang="ts">
import { WebRTCPlayer } from '@eyevinn/webrtc-player'
import { ref } from 'vue'
import { socket } from '@/socket'

const video = ref<HTMLVideoElement | null>(null)
const started = ref(false)

async function startStream(): Promise<void> {
  socket.emit('stream', { action: 'start' });
  const player = new WebRTCPlayer({
    video: video.value as HTMLVideoElement,
    type: 'whep'
  })
  await player.load(new URL(import.meta.env.VITE_STREAM_URL as string))
  started.value = true
}
</script>

<template>
  <button
    type="button"
    v-if="!started"
    @click="startStream">
    Start
  </button>
  <video v-else ref="video" autoplay muted controls playsinline></video>
</template>

<style scoped>
video {
  width: 100vw;
  height: 100vh;
}
button {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  cursor: pointer;
  outline: 0;
  text-transform: uppercase;
  color: #fff;
  background-color: #0d6efd;
  border-color: #0d6efd;
  display: inline-block;
  font-weight: bold;
  line-height: 1.5;
  text-align: center;
  border: 1px solid transparent;
  padding: 8px 14px;
  font-size: 1.4rem;
  border-radius: .25rem;
  transition: color .15s ease-in-out,background-color .15s ease-in-out,border-color .15s ease-in-out,box-shadow .15s ease-in-out;
  :hover {
      color: #fff;
      background-color: #0b5ed7;
      border-color: #0a58ca;
  }

}
</style>
