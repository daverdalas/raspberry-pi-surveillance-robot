import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';
import { WebSocketGateway } from '@nestjs/websockets';
import { ConfigService } from '@nestjs/config';
import { WebsocketsGateway } from './websockets/websockets.gateway';

function decorateGateway(
  class_: typeof WebsocketsGateway,
  config: ConfigService,
): void {
  WebSocketGateway({
    cors: {
      origin: config.get<string>('websockets.origin'),
    },
    port: config.get<number>('websockets.port'),
    host: config.get<string>('websockets.host'),
  })(class_);
}

async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  const config: ConfigService = app.get(ConfigService);
  decorateGateway(WebsocketsGateway, config);
  await app.listen(config.get<number>('server.port'));
  app.enableShutdownHooks();
}
bootstrap();
