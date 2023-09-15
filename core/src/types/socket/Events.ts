import Movement from './Movement';
import Stream from './Stream';
import Gimbal from './Gimbal';

export interface ServerToClientEvents {
}

export interface ClientToServerEvents {
  movement(e: Movement): void,
  stream(e: Stream): void,
  gimbal(e: Gimbal): void,
}
