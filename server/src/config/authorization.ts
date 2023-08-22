import { registerAs } from '@nestjs/config';

export default registerAs('authorization', () => ({
  username: process.env.STREAM_AUTHORIZATION_USERNAME,
  password: process.env.STREAM_AUTHORIZATION_PASSWORD,
}));
