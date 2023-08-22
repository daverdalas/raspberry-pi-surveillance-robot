import { registerAs } from '@nestjs/config';

export default registerAs('server', () => ({
  port: parseInt(process.env.SERVER_PORT, 10) || 3000,
}));
