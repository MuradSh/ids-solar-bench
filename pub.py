import paho.mqtt.client as mqtt
from random import randrange
import time
from datetime import datetime


class sensor:

    def __init__(self, type, id, client, broker):
        self.type = type
        self.id = id
        self.client = client
        self.broker = broker

    def send(self):
        self.client.connect(self.broker)

        while True:
            y = randrange(80, 90)
            now = datetime.now()
            dt_string = now.strftime("%Y-%m-%d %H:%M:%S") + "+07"
            data = {'datetime': dt_string,
                    'sensor id': self.id,
                    'measurement': y}

            self.client.publish("sensor_data_124", str(data))
            print("Just published " + str(data))
            time.sleep(1)


def main():
    mqttBroker = mqtt.eclipseprojects.io

    sensor_solar = sensor(type='electrical',
                          id=1,
                          client=mqtt.Client("Panel_Current"),
                          broker=mqttBroker)

    sensor_solar.send()


if __name__ == "__main__":
    main()
