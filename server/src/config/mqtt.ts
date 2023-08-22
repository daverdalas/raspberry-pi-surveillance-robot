import { registerAs } from '@nestjs/config';

export default registerAs('mqtt', () => ({
  host: process.env.MQTT_HOST,
  port: parseInt(process.env.MQTT_PORT, 10) || 1883,
  username: process.env.MQTT_USER,
  password: process.env.MQTT_PASSWORD,
  topic: process.env.MQTT_TOPIC_NAME,
}));
