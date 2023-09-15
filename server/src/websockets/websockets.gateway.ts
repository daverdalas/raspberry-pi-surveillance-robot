import {
  MessageBody,
  SubscribeMessage,
  WebSocketGateway,
} from '@nestjs/websockets';
import { MqttService } from '../mqtt/mqtt.service';
import type Stream from '@core/types/socket/Stream';
import type Movement from '@core/types/socket/Movement';
import Gimbal from '@core/types/socket/Gimbal';

@WebSocketGateway()
export class WebsocketsGateway {
  constructor(private readonly mqttService: MqttService) {}

  @SubscribeMessage('movement')
  handleEvent(@MessageBody() movement: Movement) {
    this.mqttService.movement(movement);
  }

  @SubscribeMessage('gimbal')
  handleGimbal(@MessageBody() gimbal: Gimbal) {
    this.mqttService.gimbal(gimbal);
  }

  @SubscribeMessage('stream')
  handleStream(@MessageBody() data: Stream) {
    this.mqttService.stream(data.action);
  }
}
