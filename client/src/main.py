import os
from typing import Any
import logging
import threading
import time
from mqtt_service import MQTTService
from commands.movement.movement import Movement
from commands.gimbal.gimbal import Gimbal
from commands.streamer.streamer import Streamer
import messages

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def _on_message(client: Any, userdata: Any, msg: Any) -> None:
    global last_message_time
    last_message_time = time.time()
    message = messages.Message.from_json(msg.payload)

    if isinstance(message, messages.Movement):
        movement(message.left, message.right)

        return
    if isinstance(message, messages.Gimbal):
        gimbal(message.horizontal, message.vertical, message.center)

        return
    if isinstance(message, messages.Stream):
        if message.is_start():
            streamer.start()
        elif message.is_stop():
            streamer.stop()
        return
    else:
        logger.error(f'Unknown message type: {type(message).__name__}')
        return


def _check_last_message_time() -> None:
    while True:
        time.sleep(10)
        if last_message_time and time.time() - last_message_time > 60 * 5:
            streamer.stop()


if __name__ == '__main__':
    timeout = int(os.getenv('NEXT_MESSAGE_MAX_WAIT_TIME')) / 1000
    movement = Movement(timeout=timeout)
    gimbal = Gimbal(timeout=timeout)
    last_message_time: float | None = None
    streamer = Streamer(
        stream_host=os.getenv('STREAM_HOST'),
        username=os.getenv('STREAM_AUTHORIZATION_USERNAME'),
        password=os.getenv('STREAM_AUTHORIZATION_PASSWORD'),
    )

    mqtt_service = MQTTService(
        host=os.getenv('MQTT_HOST'),
        port=os.getenv('MQTT_PORT', 1883),
        username=os.getenv('MQTT_USER'),
        password=os.getenv('MQTT_PASSWORD'),
        topic=os.getenv('MQTT_TOPIC_NAME'),
        on_message_callback=_on_message,
        logger=logger
    )
    mqtt_service.connect()

    threading.Thread(target=_check_last_message_time, daemon=True).start()

    try:
        mqtt_service.loop_forever()
    except KeyboardInterrupt:
        mqtt_service.disconnect()
        movement.cleanup()
