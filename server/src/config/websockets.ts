import { registerAs } from '@nestjs/config';

export default registerAs('websockets', () => ({
  host: process.env.WEBSOCKET_HOST,
  port: parseInt(process.env.WEBSOCKET_PORT, 10) || 3000,
  origin: process.env.WEBSOCKET_CORS_ORIGIN,
}));
