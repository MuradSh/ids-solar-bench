import paho.mqtt.client as mqtt
import time
import ast
import psycopg2

# create classes
class receiver:

    def __init__(self, name, client, broker, dbconn):
        self.name = name
        self.client = client
        self.broker = broker
        self.dbconn = dbconn

    def timescale_insert(self, message):
        cursor = self.dbconn.cursor()

        dt = message['datetime']
        id = message['sensor id']
        measurement = message['measurement']

        cursor.execute("""
                        INSERT INTO sensor_data (time, sensor_id, measurement)
                        VALUES (%s, %s, %s);
                        """,
                       (dt, id, measurement)
                       )

        self.dbconn.commit()
        cursor.close()

        print(f'inserted | {dt} | {id} | {measurement} |')

    def on_message(self, client, userdata, message):
        msg = str(message.payload.decode("utf-8"))
        msg_dictionary = ast.literal_eval(msg)

        self.timescale_insert(msg_dictionary)

        print("Received message: ", msg)

    def listen(self):
        self.client.connect(self.broker)
        self.client.loop_start()
        self.client.subscribe("sensor_data_124")
        self.client.on_message = self.on_message
        time.sleep(1000)
        self.client.loop_end()


def main():

    CONNECTION = "postgres://postgres:password@localhost:5432/iot_demo"
    conn = psycopg2.connect(CONNECTION)

    mqttBroker = "mqtt.eclipseprojects.io"
    #mqttBroker = "localhost"
    #mqttBroker = "test.mosquitto.org"
    #mqttBroker = "broker.hivemq.com"
    #mqttBroker = "192.168.100.11"
    server = receiver(name="server",
                      client=mqtt.Client("Server"),
                      broker=mqttBroker,
                      dbconn=conn)
    server.listen()


if __name__ == "__main__":
    main()
