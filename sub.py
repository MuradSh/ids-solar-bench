import paho.mqtt.client as mqtt
import time
import ast
import psycopg2

# create classes

class receiver:

    def __init__(self, name, client, broker):
        self.name = name
        self.client = client
        self.broker = broker

    def on_message(self, client, userdata, message):
        msg = str(message.payload.decode("utf-8"))
        msg_dictionary = ast.literal_eval(msg)

        print("Received message: ", msg)

    def listen(self):
        self.client.connect(self.broker)
        self.client.loop_start()
        self.client.subscribe("sensor_data_ids")
        self.client.on_message = self.on_message
        time.sleep(1000)
        self.client.loop_end()


def main():
    mqttBroker = mqtt.eclipseprojects.io
   
    server = receiver(name="server",
                      client=mqtt.Client("Server"),
                      broker=mqttBroker)
    server.listen()


if __name__ == "__main__":
    main()
