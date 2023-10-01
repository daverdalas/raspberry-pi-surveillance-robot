<script setup lang="ts">
import { onMounted, onUnmounted, ref } from 'vue'
import nipplejs from 'nipplejs'
import type Movement from '@core/types/socket/Movement'
import type Gimbal from '@core/types/socket/Gimbal'

const leftRightZone = ref<HTMLElement | null>(null)
let leftRightManager: nipplejs.JoystickManager | null = null
const upDownZone = ref<HTMLElement | null>(null)
let upDownManager: nipplejs.JoystickManager | null = null
const gimbalZone = ref<HTMLElement | null>(null)
let gimbalManager: nipplejs.JoystickManager | null = null
let upDownValue = 0
let leftRightValue = 0
const MAX_DISTANCE = 50

const emit = defineEmits<{
  (event: 'movement', payload: Movement): void
  (event: 'gimbal', payload: Gimbal): void
}>()

onMounted(() => {
  initUpDown()
  initLeftRight()
  initGimbal()
})

function initUpDown(): void {
  upDownManager = nipplejs.create({
    zone: upDownZone.value as HTMLElement,
    mode: 'static',
    position: { right: '80px', bottom: '90px' },
    color: 'red',
    size: 100,
    lockY: true
  })
  upDownManager.on('move', (evt, data) => {
    if (data.direction) {
      upDownValue = data.direction.angle === 'up' ? data.distance : -data.distance
      emitMovementDirection()

      return
    }

    upDownValue = 0
    emitMovementDirection()
  })
  upDownManager.on('end', () => {
    upDownValue = 0
    emitMovementDirection()
  })
}

function initLeftRight(): void {
  leftRightManager = nipplejs.create({
    zone: leftRightZone.value as HTMLElement,
    mode: 'static',
    position: { left: '80px', bottom: '90px' },
    color: 'red',
    size: 100,
    lockX: true
  })
  leftRightManager.on('move', (evt, data) => {
    if (data.direction) {
      leftRightValue = data.direction.angle === 'right' ? data.distance : -data.distance
      emitMovementDirection()

      return
    }

    leftRightValue = 0
    emitMovementDirection()
  })
  leftRightManager.on('end', () => {
    leftRightValue = 0
    emitMovementDirection()
  })
}

function initGimbal(): void {
  gimbalManager = nipplejs.create({
    zone: gimbalZone.value as HTMLElement,
    mode: 'static',
    position: { right: '70px', top: '60px' },
    color: 'red',
    size: 70,
    restOpacity: 0.3
  })
  gimbalManager.on('move', (evt, data) => {
    const horizontalSpeedFactor = 3,
      verticalSpeedFactor = 2
    const angleDeg = data.angle.degree
    const distance = data.distance / MAX_DISTANCE
    const horizontal = -Math.cos(angleDeg * (Math.PI / 180)) * distance * horizontalSpeedFactor
    const vertical = Math.sin(angleDeg * (Math.PI / 180)) * distance * verticalSpeedFactor

    emit('gimbal', { horizontal, vertical })
  })
  gimbalManager.on('end', () => {
    emit('gimbal', { horizontal: 0, vertical: 0 })
  })
}

function centerGimbal(): void {
  emit('gimbal', { horizontal: 0, vertical: 0, center: true })
}

function emitMovementDirection(): void {
  const maxSpeed = 0.3,
    minSpeed = 0.065
  let speedRange = maxSpeed - minSpeed

  if (!upDownValue && !leftRightValue) {
    emit('movement', { left: 0, right: 0 })
    return
  }

  let movementSpeed =
    ((Math.abs(upDownValue) / MAX_DISTANCE) * speedRange + minSpeed) * Math.sign(upDownValue)
  let turnSpeed =
    ((Math.abs(leftRightValue) / MAX_DISTANCE) * speedRange + minSpeed) * Math.sign(leftRightValue)

  if (upDownValue && !leftRightValue) {
    return emit('movement', { left: movementSpeed, right: movementSpeed })
  }

  if (!upDownValue && leftRightValue) {
    return emit('movement', { left: turnSpeed, right: -turnSpeed })
  }

  speedRange = movementSpeed - minSpeed
  turnSpeed = (Math.abs(leftRightValue) / MAX_DISTANCE) * speedRange + minSpeed
  turnSpeed = Math.abs(movementSpeed - (turnSpeed - minSpeed)) * Math.sign(upDownValue)

  let left = leftRightValue > 0 ? movementSpeed : turnSpeed
  let right = leftRightValue > 0 ? turnSpeed : movementSpeed

  emit('movement', { left, right })
}

onUnmounted(() => {
  if (leftRightManager) leftRightManager.destroy()
  if (upDownManager) upDownManager.destroy()
})
</script>

<template>
  <div id="left-right-zone" class="zone" ref="leftRightZone" />
  <div id="gimbal-zone" class="zone" ref="gimbalZone">
    <div id="center-button" @click="centerGimbal">
      <font-awesome-icon :icon="['fas', 'arrows-to-dot']" />
    </div>
  </div>
  <div id="up-down-zone" class="zone" ref="upDownZone" />
</template>

<style scoped>
.zone {
  height: 50%;
  width: 30%;
  min-width: 150px;
  position: absolute;
}

#up-down-zone {
  right: 0;
  bottom: 0;
}

#left-right-zone {
  left: 0;
  bottom: 0;
}

#gimbal-zone {
  top: 0;
  right: 0;
}

#center-button {
  position: absolute;
  top: 90px;
  right: 15px;
  font-size: 1.3em;
  background: rgb(128, 128, 128);
  border-radius: 50%;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid red;
  opacity: 0.4;
  z-index: 1;
}
</style>
