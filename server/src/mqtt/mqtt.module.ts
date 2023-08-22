import { Module } from '@nestjs/common';
import { ClientsModule, Transport } from '@nestjs/microservices';
import { ConfigModule, ConfigService } from '@nestjs/config';
import { MqttService } from './mqtt.service';
import providers from './providers';

@Module({
  imports: [
    ClientsModule.registerAsync([
      {
        name: providers.MQTT,
        imports: [ConfigModule],
        inject: [ConfigService],
        useFactory: (configService: ConfigService) => ({
          transport: Transport.MQTT,
          options: {
            url: `mqtt://${configService.get<string>(
              'mqtt.host',
            )}:${configService.get<number>('mqtt.port')}`,
            username: configService.get<string>('mqtt.username'),
            password: configService.get<string>('mqtt.password'),
          },
        }),
      },
    ]),
  ],
  providers: [MqttService],
  exports: [MqttService],
})
export class MqttModule {}
