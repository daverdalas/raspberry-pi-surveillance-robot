<script setup lang="ts">
import { onMounted, onUnmounted } from 'vue'
import Keyboard from '@/components/RobotMovement/Keyboard.vue'
import { socket } from '@/socket'
import type Movement from '@core/types/socket/Movement'
import type Gimbal from '@core/types/socket/Gimbal'
import { isEqual } from 'lodash'
import Mobile from '@/components/RobotMovement/Mobile.vue'
import { isMobile } from '@/state'

const interval: number = (import.meta.env.VITE_NEXT_MESSAGE_MAX_WAIT_TIME as number) / 2

const STOP_GIMBAL: Gimbal = { vertical: 0, horizontal: 0, center: false }
const STOP_MOVEMENT: Movement = { left: 0, right: 0 }

let lastGimbalEvent: Gimbal = STOP_GIMBAL
let lastMovementEvent: Movement = STOP_MOVEMENT

let gimbalIntervalId: number | null = null
let movementIntervalId: number | null = null

function sendEvent(eventName: 'gimbal' | 'movement', payload: any, lastEvent: any) {
  if (!isEqual(payload, lastEvent)) {
    socket.emit(eventName, payload)
  }

  return payload
}

function gimbal(payload: Gimbal): void {
  lastGimbalEvent = sendEvent('gimbal', payload, lastGimbalEvent)
}

function movement(payload: Movement): void {
  lastMovementEvent = sendEvent('movement', payload, lastMovementEvent)
}

onMounted(() => {
  gimbalIntervalId = setInterval(() => {
    if (!isEqual(lastGimbalEvent, STOP_GIMBAL)) {
      socket.emit('gimbal', lastGimbalEvent)
    }
  }, interval)

  movementIntervalId = setInterval(() => {
    if (!isEqual(lastMovementEvent, STOP_MOVEMENT)) {
      socket.emit('movement', lastMovementEvent)
    }
  }, interval)
})

onUnmounted(() => {
  if (gimbalIntervalId) clearInterval(gimbalIntervalId)
  if (movementIntervalId) clearInterval(movementIntervalId)
})
</script>

<template>
  <Mobile v-if="isMobile" @gimbal="gimbal" @movement="movement" />
  <Keyboard v-else @gimbal="gimbal" @movement="movement" />
</template>

<style scoped>
div {
  display: none;
}
</style>
