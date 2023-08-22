import {
  MessageBody,
  SubscribeMessage,
  WebSocketGateway,
} from '@nestjs/websockets';
import { MqttService } from '../mqtt/mqtt.service';

@WebSocketGateway()
export class WebsocketsGateway {
  constructor(private readonly mqttService: MqttService) {}

  @SubscribeMessage('movement')
  handleEvent(@MessageBody('direction') direction: string) {
    this.mqttService.movement(direction);
  }

  @SubscribeMessage('gimbal')
  handleGimbal(@MessageBody('direction') direction: string) {
    this.mqttService.gimbal(direction);
  }
}
