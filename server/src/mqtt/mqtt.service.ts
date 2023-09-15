import { Inject, Injectable } from '@nestjs/common';
import { ClientProxy } from '@nestjs/microservices';
import { ConfigService } from '@nestjs/config';
import providers from './providers';
import Movement from '@core/types/socket/Movement';
import Gimbal from '@core/types/socket/Gimbal';

@Injectable()
export class MqttService {
  private readonly topicName: string;

  constructor(
    @Inject(providers.MQTT) private client: ClientProxy,
    configService: ConfigService,
  ) {
    this.topicName = configService.get<string>('mqtt.topic');
  }

  async onApplicationBootstrap(): Promise<void> {
    await this.client.connect();
  }

  movement(movement: Movement): void {
    this.client.emit(this.topicName, {
      type: 'movement',
      ...movement,
    });
  }

  gimbal(gimbal: Gimbal): void {
    this.client.emit(this.topicName, {
      type: 'gimbal',
      ...gimbal,
    });
  }

  stream(action: string): void {
    this.client.emit(this.topicName, {
      type: 'stream',
      action,
    });
  }
}
