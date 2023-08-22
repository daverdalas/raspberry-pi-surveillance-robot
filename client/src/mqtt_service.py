import paho.mqtt.client as mqtt

class MQTTService:
    def __init__(self, host, port, username, password, topic, on_message_callback, keepalive=60):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.topic = topic
        self.on_message_callback = on_message_callback
        self.keepalive = keepalive
        self.client = mqtt.Client()
        self.client.username_pw_set(self.username, self.password)

    def __on_connect(self, client, userdata, flags, rc):
        print('Connected with result code '+str(rc))
        client.subscribe(self.topic)

    def connect(self):
        self.client.on_connect = self.__on_connect
        self.client.on_message = self.on_message_callback
        self.client.connect(self.host, self.port, self.keepalive)

    def publish(self, payload):
        self.client.publish(self.topic, payload=payload, qos=0)

    def loop_forever(self):
        self.client.loop_forever()
