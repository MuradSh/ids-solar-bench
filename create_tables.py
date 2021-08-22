import psycopg2


def createTables(conn):
    cursor = conn.cursor()
    with open('create_tables.sql', 'r') as f:
        cursor.execute(f.read())
        print(f.read())
    f.close()

    cursor.execute("SELECT * FROM sensors")
    print(cursor.fetchone())

    cursor.execute("SELECT * FROM sensor_data")
    print(cursor.fetchone())

    conn.commit()
    return cursor


def main():
    CONNECTION = "postgres://postgres:password@localhost:5432/iot_demo"
    conn = psycopg2.connect(CONNECTION)
    cursor = createTables(conn)
    cursor.close()


if __name__ == "__main__":
    main()
