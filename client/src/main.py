try:
    import RPi.GPIO as GPIO
except (RuntimeError, ModuleNotFoundError):
    import sys
    import fake_rpi

    sys.modules['RPi'] = fake_rpi.RPi  # Fake RPi
    sys.modules['RPi.GPIO'] = fake_rpi.RPi.GPIO  # Fake GPIO
    sys.modules['smbus'] = fake_rpi.smbus  # Fake smbus (I2C)
    import RPi.GPIO as GPIO
from mqtt_service import MQTTService
from commands.movement.movement import Movement
from commands.gimbal.gimbal import Gimbal
import messages
import os

timeout = int(os.getenv('NEXT_MESSAGE_MAX_WAIT_TIME')) / 1000
movement = Movement(gpio=GPIO, timeout=timeout)
gimbal = Gimbal(gpio=GPIO, timeout=timeout)


def on_message(client, userdata, msg):
    message = messages.Message.from_json(msg.payload)
    if isinstance(message, messages.Movement):
        service = movement
    elif isinstance(message, messages.Gimbal):
        service = gimbal
    else:
        raise Exception('Unknown message type')
    if getattr(service, message.direction()):
        getattr(service, message.direction())()
    else:
        raise Exception('Unknown direction')


if __name__ == '__main__':
    mqtt_service = MQTTService(
        host=os.getenv('MQTT_HOST'),
        port=os.getenv('MQTT_PORT', 1883),
        username=os.getenv('MQTT_USER'),
        password=os.getenv('MQTT_PASSWORD'),
        topic=os.getenv('MQTT_TOPIC_NAME'),
        on_message_callback=on_message
    )
    mqtt_service.connect()

    try:
        mqtt_service.loop_forever()
    except KeyboardInterrupt:
        movement.cleanup()
        gimbal.cleanup()
        GPIO.cleanup()
