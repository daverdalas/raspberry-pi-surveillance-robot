import paho.mqtt.client as mqtt
import logging
import time
from typing import Callable, Any


class MQTTService:
    _host: str
    _port: int
    _username: str
    _password: str
    _topic: str
    _keepalive: int
    _client: mqtt.Client
    _logger: logging.Logger
    _on_message_callback: Callable[[mqtt.Client, Any, mqtt.MQTTMessage], None]

    def __init__(self,
                 host: str,
                 port: int,
                 username: str,
                 password: str,
                 topic: str,
                 on_message_callback: Callable[[mqtt.Client, Any, mqtt.MQTTMessage], None],
                 logger: logging.Logger,
                 keepalive: int = 60
                 ) -> None:
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

    def _on_connect(self, client: mqtt.Client, userdata: Any, flags: dict, rc: int) -> None:
        self._logger.info(f'Connected with result code {rc}')
        client.subscribe(self._topic)

    def connect(self, retries: int = 5, delay: int = 5) -> None:
        self._client.on_connect = self._on_connect
        self._client.on_message = self._on_message_callback

        for _ in range(retries):
            try:
                self._client.connect(self._host, self._port, self._keepalive)
                return
            except Exception as e:
                self._logger.error(f"Failed to connect. Attempting again in {delay} seconds. Error: {e}")
                time.sleep(delay)

        raise RuntimeError("Failed to connect to MQTT after multiple attempts.")

    def disconnect(self) -> None:
        self._client.disconnect()

    def publish(self, payload: str) -> None:
        self._client.publish(self._topic, payload=payload, qos=0)

    def loop_forever(self) -> None:
        self._client.loop_forever()
