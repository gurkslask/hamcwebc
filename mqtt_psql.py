"""Module for inserting mqtt values to postgresql server"""
import paho.mqtt.client as mqtt
import psycopg2

def on_connect(client, userdata, flags, rc):
    """Subscribe on connect."""
    client.subscribe('kgrund/fukt')
    client.subscribe('kgrund/temp')


def on_message(client, userdata, msg):
    """Callback on new message."""
    msg.topic = str(msg.topic).replace('/', '_')
    print(msg.topic + str(msg.payload))

    conn = psycopg2.connect(
            dbname='alex',
            user='alex',
            password='bit',
            host='192.168.1.19')
    cur = conn.cursor()
    sensor_id = None
    print(msg.topic)
    cur.execute("SELECT id FROM sensors WHERE name = '{}'".format(msg.topic))
    sensor_id = cur.fetchone()
    print(sensor_id)
    if sensor_id:
        cur.execute(
            ' UPDATE sensors SET value = %s WHERE id = %s',
            (float(msg.payload), sensor_id)
        )
    else:

        cur.execute(
            ' INSERT INTO sensors (name, value) VALUES (%s, %s) ',
            (msg.topic, float(msg.payload))
        )
    # cur.execute('SELECT id FROM sensors WHERE name = "%s"')
    # id = cur.fetchone()
    # print(id)
    # cur.execute(
    # ' INSERT INTO sensortimedata (name, value) VALUES (%s, %s) ',
    # (msg.topic, float(msg.payload))
    # )
    conn.commit()
    cur.close()
    conn.close()

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

if __name__ == '__main__':
    client.connect_async('192.168.1.19', 1883, 60)
    client.loop_forever()
    # postgresql://alex:bit@127.0.0.1:5432/alex
