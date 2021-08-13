# This script serves to test the connection with the timesclaedb database
from os import name
import numpy as np
from random import uniform
import time
from numpy.lib.function_base import insert
import psycopg2
from datetime import datetime


class sensor:
    def __init__(self, type, id, conn):
        self.type = type
        self.id = id
        self.conn = conn

    # function to simulate data in real time with timestamps
    def generate(self, type, id, conn):
        x = 0

        if type == 'electrical':

            while True:
                y = (np.sin(np.pi/5*x) + np.sin(np.pi/10*x)) \
                    * uniform(-1.5, 1.5)*5 + 100

                y = round(y, 3)

                now = datetime.now()
                dt_string = now.strftime("%Y-%m-%d %H:%M:%S")

                input = {'dt': dt_string, 'sensor_id': id, 'measurement': y}
                sensor.timescale_insert(input, conn)

                x += 1
                time.sleep(2)

    def timescale_insert(input, conn):
        cursor = conn.cursor()

        dt = input['dt']
        id = input['sensor_id']
        measurement = input['measurement']

        cursor.execute("""
                        INSERT INTO sensor_data (time, sensor_id, measurement)
                        VALUES (%s, %s, %s);
                        """,
                       (dt, id, measurement)
                       )

        conn.commit()
        cursor.close()

        print(f'inserting | {dt} | {id} | {measurement} |')


def testConnection(cursor):
    # use the cursor to interact with your database
    cursor.execute("SELECT 'hello world'")
    print(cursor.fetchone())


def main():

    CONNECTION = "postgres://postgres:password@localhost:5432/iot_demo"
    conn = psycopg2.connect(CONNECTION)

    testConnection(conn.cursor())
    sensor_solar = sensor(type='electrical', id=1, conn=conn)
    sensor_solar.generate(
        sensor_solar.type, sensor_solar.id, sensor_solar.conn)


if __name__ == "__main__":
    main()
