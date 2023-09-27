<script setup lang="ts">
import { onMounted, onUnmounted } from 'vue'
import type Movement from '@core/types/socket/Movement'
import type Gimbal from '@core/types/socket/Gimbal'

let keysPressed = new Set<string>()

const emit = defineEmits<{
  (event: 'gimbal', payload: Gimbal): void
  (event: 'movement', payload: Movement): void
}>()

onMounted((): void => {
  document.addEventListener('keydown', handleKeydown)
  document.addEventListener('keyup', handleKeyup)
})

onUnmounted((): void => {
  document.removeEventListener('keydown', handleKeydown)
  document.removeEventListener('keyup', handleKeyup)
})

function handleKeydown(e: KeyboardEvent): void {
  keysPressed.add(e.key)
  emitDirections(e.key)
}

function handleKeyup(e: KeyboardEvent): void {
  keysPressed.delete(e.key)
  emitDirections(e.key)
}

function isGimbalKey(key: string): boolean {
  return Object.values(gimbalKeys).includes(key)
}

function isMovementKey(key: string): boolean {
  return Object.values(movementKeys).includes(key)
}

function emitDirections(key: string): void {
  if (isGimbalKey(key)) {
    sendGimbalDirection()

    return
  }

  if (isMovementKey(key)) {
    emitMovementDirection()

    return
  }
}

function emitMovementDirection(): void {
  const direction = movementDirection()
  emit('movement', direction)
}

function sendGimbalDirection(): void {
  const direction = gimbalDirection()
  emit('gimbal', direction)
}

function movementDirection(): Movement {
  const direction = determineDirection(movementKeys)

  const movementMapping: { [key in Direction]: Movement } = {
    [Direction.UP]: { left: 0.25, right: 0.25 },
    [Direction.DOWN]: { left: -0.25, right: -0.25 },
    [Direction.LEFT]: { left: -0.25, right: 0.25 },
    [Direction.RIGHT]: { left: 0.25, right: -0.25 },
    [Direction.UP_LEFT]: { left: 0.065, right: 0.25 },
    [Direction.UP_RIGHT]: { left: 0.25, right: 0.065 },
    [Direction.DOWN_LEFT]: { left: -0.065, right: -0.25 },
    [Direction.DOWN_RIGHT]: { left: -0.25, right: -0.065 },
    [Direction.STOP]: { left: 0, right: 0 }
  }

  return movementMapping[direction]
}

function gimbalDirection(): Gimbal {
  const direction = determineDirection(gimbalKeys)
  const center = keysPressed.has(gimbalKeys.center)

  const movementMapping: { [key in Direction]: Gimbal } = {
    [Direction.UP]: { horizontal: 0, vertical: 2 },
    [Direction.DOWN]: { horizontal: 0, vertical: -2 },
    [Direction.LEFT]: { horizontal: 3, vertical: 0 },
    [Direction.RIGHT]: { horizontal: -3, vertical: 0 },
    [Direction.UP_LEFT]: { horizontal: 3, vertical: 2 },
    [Direction.UP_RIGHT]: { horizontal: -3, vertical: 2 },
    [Direction.DOWN_LEFT]: { horizontal: 3, vertical: -2 },
    [Direction.DOWN_RIGHT]: { horizontal: -3, vertical: -2 },
    [Direction.STOP]: { horizontal: 0, vertical: 0 }
  }

  return { ...movementMapping[direction], center }
}

function determineDirection(keys: FourDirectionKeys): Direction {
  const vertical = keysPressed.has(keys.up)
    ? Direction.UP
    : keysPressed.has(keys.down)
    ? Direction.DOWN
    : Direction.STOP
  const horizontal = keysPressed.has(keys.left)
    ? Direction.LEFT
    : keysPressed.has(keys.right)
    ? Direction.RIGHT
    : Direction.STOP

  if (vertical === Direction.STOP && horizontal === Direction.STOP) {
    return Direction.STOP
  }

  if (vertical !== Direction.STOP && horizontal !== Direction.STOP) {
    return Direction[`${Direction[vertical]}_${Direction[horizontal]}` as keyof typeof Direction]
  }

  return vertical !== Direction.STOP ? vertical : horizontal
}

enum Direction {
  UP,
  DOWN,
  LEFT,
  RIGHT,
  UP_LEFT,
  UP_RIGHT,
  DOWN_LEFT,
  DOWN_RIGHT,
  STOP
}

interface FourDirectionKeys {
  up: string
  down: string
  left: string
  right: string
}

interface GimbalKeys extends FourDirectionKeys {
  center: string
}

const gimbalKeys: GimbalKeys = {
  up: 'w',
  down: 's',
  left: 'a',
  right: 'd',
  center: 'c'
}

const movementKeys: FourDirectionKeys = {
  up: 'ArrowUp',
  down: 'ArrowDown',
  left: 'ArrowLeft',
  right: 'ArrowRight'
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
