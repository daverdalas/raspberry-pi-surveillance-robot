import { Inject, Injectable } from '@nestjs/common';
import { ClientProxy } from '@nestjs/microservices';
import { ConfigService } from '@nestjs/config';
import providers from './providers';

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

  movement(direction: string): void {
    this.client.emit(this.topicName, {
      type: 'movement',
      direction,
    });
  }

  gimbal(direction: string): void {
    this.client.emit(this.topicName, {
      type: 'gimbal',
      direction,
    });
  }
}
