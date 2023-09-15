<script setup lang="ts">
import { onMounted, onUnmounted } from 'vue'
import { socket } from '@/socket'
import type Movement from '@core/types/socket/Movement'
import type Gimbal from '@core/types/socket/Gimbal'

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
    socket.emit('gimbal', { vertical: 0, horizontal: 0, center: true })
  }

  if (keysPressed.size === 0) {
    stopAll()

    return
  }

  sendDirections()
}

function pollingCheck(): void {
  const elapsedTime = Date.now() - lastKeyActionTimestamp

  // If no key event was recorded for a duration longer than the timeout, stop everything
  if (elapsedTime >= timeout) {
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
    socket.emit('movement', direction)
  }
}

function sendGimbalDirection(): void {
  const direction = gimbalDirection()

  if (direction) {
    socket.emit('gimbal', direction)
  }
}

function movementDirection(): Movement | null {
  const direction = determineDirection('ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight')

  const movementMapping: { [key in Direction]: Movement } = {
    [Direction.UP]: { left: 0.25, right: 0.25 },
    [Direction.DOWN]: { left: -0.25, right: -0.25 },
    [Direction.LEFT]: { left: -0.25, right: 0.25 },
    [Direction.RIGHT]: { left: 0.25, right: -0.25 },
    [Direction.UP_LEFT]: { left: 0.065, right: 0.25 },
    [Direction.UP_RIGHT]: { left: 0.25, right: 0.065 },
    [Direction.DOWN_LEFT]: { left: -0.065, right: -0.25 },
    [Direction.DOWN_RIGHT]: { left: -0.25, right: -0.065 }
  }

  return direction !== null ? movementMapping[direction] : null
}

function gimbalDirection(): Gimbal | null {
  const direction = determineDirection('w', 's', 'a', 'd')

  const movementMapping: { [key in Direction]: Gimbal } = {
    [Direction.UP]: { horizontal: 0, vertical: 2 },
    [Direction.DOWN]: { horizontal: 0, vertical: -2 },
    [Direction.LEFT]: { horizontal: 3, vertical: 0 },
    [Direction.RIGHT]: { horizontal: -3, vertical: 0 },
    [Direction.UP_LEFT]: { horizontal: 3, vertical: 2 },
    [Direction.UP_RIGHT]: { horizontal: -3, vertical: 2 },
    [Direction.DOWN_LEFT]: { horizontal: 3, vertical: -2 },
    [Direction.DOWN_RIGHT]: { horizontal: -3, vertical: -2 }
  }

  return direction !== null ? movementMapping[direction] : null
}

enum Direction {
  UP,
  DOWN,
  LEFT,
  RIGHT,
  UP_LEFT,
  UP_RIGHT,
  DOWN_LEFT,
  DOWN_RIGHT
}

function determineDirection(
  upKey: string,
  downKey: string,
  leftKey: string,
  rightKey: string
): Direction | null {
  const vertical = keysPressed.has(upKey)
    ? Direction.UP
    : keysPressed.has(downKey)
    ? Direction.DOWN
    : null
  const horizontal = keysPressed.has(leftKey)
    ? Direction.LEFT
    : keysPressed.has(rightKey)
    ? Direction.RIGHT
    : null

  if (vertical === null && horizontal === null) {
    return null
  }

  if (vertical !== null && horizontal !== null) {
    return Direction[`${Direction[vertical]}_${Direction[horizontal]}` as keyof typeof Direction]
  }

  return vertical !== null ? vertical : horizontal
}

function stopAll(): void {
  clearInterval(intervalId!)
  intervalId = null

  socket.emit('movement', { left: 0, right: 0 })
  socket.emit('gimbal', { horizontal: 0, vertical: 0 })
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
