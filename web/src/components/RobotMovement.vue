<script setup lang="ts">
import { onMounted, onUnmounted } from 'vue'
import { socket } from '@/socket'

let intervalId: number | null = null
let keysPressed = new Set<string>()
const messageInterval: number = (import.meta.env.VITE_NEXT_MESSAGE_MAX_WAIT_TIME as number) / 2
const timeout: number = 600
let lastKeyActionTimestamp = 0

onMounted((): void => {
  document.addEventListener('keydown', handleKeydown)
  document.addEventListener('keyup', handleKeyup)
})

onUnmounted((): void => {
  document.removeEventListener('keydown', handleKeydown)
  document.removeEventListener('keyup', handleKeyup)

  if (intervalId !== null) {
    clearInterval(intervalId)
  }
})

function handleKeydown(e: KeyboardEvent): void {
  keysPressed.add(e.key)
  console.log(Date.now() - lastKeyActionTimestamp)
  lastKeyActionTimestamp = Date.now()

  if (!intervalId) {
    sendDirections()
    intervalId = setInterval(pollingCheck, messageInterval)
  }
}

function handleKeyup(e: KeyboardEvent): void {
  keysPressed.delete(e.key)
  lastKeyActionTimestamp = Date.now()

  if (e.key === 'c') {
    socket.emit('gimbal', { direction: 'center' })
  }

  if (keysPressed.size === 0) {
    stopAll()
  } else {
    sendDirections()
  }
}

function pollingCheck(): void {
  const elapsedTime = Date.now() - lastKeyActionTimestamp

  // If no key event was recorded for a duration longer than the timeout, stop everything
  if (elapsedTime >= timeout) {
    console.log('timeout')
    stopAll()
    return
  }

  sendDirections()
}

function sendDirections(): void {
  sendMovementDirection()
  sendGimbalDirection()
}

function sendMovementDirection(): void {
  const direction = movementDirection()
  if (direction) {
    socket.emit('movement', { direction })
  }
}

function sendGimbalDirection(): void {
  const direction = gimbalDirection()
  if (direction) {
    socket.emit('gimbal', { direction })
  }
}

function movementDirection(): string | null {
  return directions('ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight')
}

function gimbalDirection(): string | null {
  return directions('w', 's', 'a', 'd')
}

function directions(
  upKey: string,
  downKey: string,
  leftKey: string,
  rightKey: string
): string | null {
  const vertical = keysPressed.has(upKey) ? 'up' : keysPressed.has(downKey) ? 'down' : ''
  const horizontal = keysPressed.has(leftKey) ? 'left' : keysPressed.has(rightKey) ? 'right' : ''

  return [vertical, horizontal].filter(Boolean).join('_') || null
}

function stopAll(): void {
  clearInterval(intervalId!)
  intervalId = null

  socket.emit('movement', { direction: 'stop' })
  socket.emit('gimbal', { direction: 'stop' })
}
</script>

<template>
  <div />
</template>

<style scoped>
div {
  display: none;
}
</style>
