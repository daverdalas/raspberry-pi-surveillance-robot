import { reactive } from 'vue'
import { io, Socket } from 'socket.io-client'
import type { ClientToServerEvents, ServerToClientEvents } from '@core/types/socket/Events'

interface State {
  connected: boolean
}

export const state: State = reactive({
  connected: false
})

const URL: string = import.meta.env.VITE_WEBSOCKET_URL as string

export const socket: Socket<ServerToClientEvents, ClientToServerEvents> = io(URL)

socket.on('connect', () => {
  state.connected = true
})

socket.on('disconnect', () => {
  state.connected = false
})
