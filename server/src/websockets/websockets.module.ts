import { Module } from '@nestjs/common';
import { WebsocketsGateway } from './websockets.gateway';
import { MqttModule } from '../mqtt/mqtt.module';

@Module({
  providers: [WebsocketsGateway],
  imports: [MqttModule],
})
export class WebsocketsModule {}
