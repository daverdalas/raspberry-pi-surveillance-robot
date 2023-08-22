<script setup lang="ts">
import { WebRTCPlayer } from '@eyevinn/webrtc-player'
import { onMounted, ref } from 'vue'

const video = ref<HTMLVideoElement | null>(null)

onMounted(async (): Promise<void> => {
  const player = new WebRTCPlayer({
    video: video.value as HTMLVideoElement,
    type: 'whep'
  })
  await player.load(new URL(import.meta.env.VITE_STREAM_URL as string))
})
</script>

<template>
  <video ref="video" autoplay muted controls playsinline></video>
</template>

<style scoped>
video {
  width: 100vw;
  height: 100vh;
}
</style>
