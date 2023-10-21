<script setup lang="ts">
import RobotMovement from '@/components/RobotMovement/Index.vue'
import StreamPlayer from '@/components/StreamPlayer.vue'
import { isMobile, started } from '@/state'

function start(): void {
  started.value = true

  if (isMobile.value) {
    setupFullScreenAndLockOrientation()
  }
}

async function setupFullScreenAndLockOrientation(): Promise<void> {
  try {
    // Go full screen
    const elem = document.documentElement
    const methodToBeInvoked =
      elem.requestFullscreen || // @ts-ignore
      elem.mozRequestFullScreen || // @ts-ignore
      elem.webkitRequestFullscreen || // @ts-ignore
      elem.msRequestFullscreen
    await methodToBeInvoked.call(elem)

    // Lock screen orientation
    await screen.orientation.lock('landscape-primary')
  } catch (err) {
    console.error(`Failed to setup full screen and lock orientation: ${err}`)
  }
}
</script>

<template>
  <main>
    <button class="start-button" type="button" v-if="!started" @click="start">Start</button>
    <RobotMovement v-if="started" />
    <StreamPlayer v-if="started" />
  </main>
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
</style>
