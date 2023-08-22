import { reactive } from 'vue'
import { io, Socket } from 'socket.io-client'

interface State {
  connected: boolean
  fooEvents: Array<any>
  barEvents: Array<any>
}

export const state: State = reactive({
  connected: false,
  fooEvents: [],
  barEvents: []
})

const URL: string = import.meta.env.VITE_WEBSOCKET_URL as string

export const socket: Socket = io(URL)

socket.on('connect', () => {
  state.connected = true
})

socket.on('disconnect', () => {
  state.connected = false
})
