<script setup lang="ts">
import { onMounted, onUnmounted, ref } from 'vue'
import nipplejs from 'nipplejs'
import type Movement from '@core/types/socket/Movement'

const leftRightZone = ref<HTMLElement | null>(null)
let leftRightManager: nipplejs.JoystickManager | null = null
const upDownZone = ref<HTMLElement | null>(null)
let upDownManager: nipplejs.JoystickManager | null = null
let upDownValue = 0
let leftRightValue = 0

const emit = defineEmits<{
  (event: 'movement', payload: Movement): void
}>()

onMounted(() => {
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
})

function emitMovementDirection(): void {
  const maxSpeed = 0.3, minSpeed = 0.065;
  let speedRange = maxSpeed - minSpeed;

  if (!upDownValue && !leftRightValue) {
    emit('movement', { left: 0, right: 0 });
    return;
  }

  let movementSpeed = ((Math.abs(upDownValue) / 50) * speedRange + minSpeed) * Math.sign(upDownValue);
  let turnSpeed = ((Math.abs(leftRightValue) / 50) * speedRange + minSpeed) * Math.sign(leftRightValue);

  if (upDownValue && !leftRightValue) {
    return emit('movement', { left: movementSpeed, right: movementSpeed });
  }

  if (!upDownValue && leftRightValue) {
    return emit('movement', { left: turnSpeed, right: -turnSpeed });
  }

  speedRange = movementSpeed - minSpeed;
  turnSpeed = (Math.abs(leftRightValue) / 50) * speedRange + minSpeed;
  turnSpeed = Math.abs((movementSpeed - (turnSpeed - minSpeed))) * Math.sign(upDownValue);

  let left = leftRightValue > 0 ? movementSpeed : turnSpeed;
  let right = leftRightValue > 0 ? turnSpeed : movementSpeed;

  emit('movement', { left, right });
}

onUnmounted(() => {
  if (leftRightManager) leftRightManager.destroy()
  if (upDownManager) upDownManager.destroy()
})
</script>

<template>
  <div id="up-down-zone" ref="upDownZone"></div>
  <div id="left-right-zone" ref="leftRightZone"></div>
</template>

<style scoped>
#up-down-zone {
  height: 50%;
  width: 30%;
  min-width: 300px;
  max-width: 50%;
  position: absolute;
  right: 0;
  bottom: 0;
}

#left-right-zone {
  height: 100%;
  width: 30%;
  min-width: 300px;
  max-width: 50%;
  position: absolute;
  left: 0;
  bottom: 0;
}
</style>
