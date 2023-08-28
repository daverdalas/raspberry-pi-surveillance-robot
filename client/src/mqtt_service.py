import paho.mqtt.client as mqtt
import logging


class MQTTService:
    def __init__(self,
                 host: str,
                 port: int,
                 username: str,
                 password: str,
                 topic: str,
                 on_message_callback,
                 logger: logging.Logger,
                 keepalive: int = 60,
                 ):
        self._host = host
        self._port = port
        self._username = username
        self._password = password
        self._topic = topic
        self._on_message_callback = on_message_callback
        self._keepalive = keepalive
        self._client = mqtt.Client()
        self._client.username_pw_set(self._username, self._password)
        self._logger = logger

    def _on_connect(self, client, userdata, flags, rc):
        self._logger.info(f'Connected with result code {rc}')
        client.subscribe(self._topic)

    def connect(self):
        self._client.on_connect = self._on_connect
        self._client.on_message = self._on_message_callback
        self._client.connect(self._host, self._port, self._keepalive)

    def disconnect(self):
        self._client.disconnect()

    def publish(self, payload: str):
        self._client.publish(self._topic, payload=payload, qos=0)

    def loop_forever(self):
        self._client.loop_forever()
