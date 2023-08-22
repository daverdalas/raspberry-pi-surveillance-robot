import { Module } from '@nestjs/common';
import { ConfigModule } from '@nestjs/config';
import mqtt from './config/mqtt';
import websockets from './config/websockets';
import { WebsocketsModule } from './websockets/websockets.module';
import { AuthorizationModule } from './authorization/authorization.module';
import server from './config/server';
import authorization from './config/authorization';

@Module({
  imports: [
    ConfigModule.forRoot({
      load: [mqtt, websockets, server, authorization],
      ignoreEnvFile: true,
      isGlobal: true,
    }),
    WebsocketsModule,
    AuthorizationModule,
  ],
})
export class AppModule {}
