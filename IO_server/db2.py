"""Database connections."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Sensor, SensorTimeData

import paho.mqtt.client as mqtt


def put_sql(name, value):
    """Connect to sql and put in values."""
    session = Session()

    sensor = session.query(Sensor).filter(Sensor.name == name).first()
    print(sensor)

    if sensor:
        """Make timesensor post."""
        time_data = SensorTimeData(data=value)
        sensor.timedata = sensor.timedata + [time_data]
        session.add(time_data)

        sensor.value = value
        session.add(sensor)
    else:
        sensor(name=name, value=value)
        session.add(sensor)

    session.commit()
    session.close()


def on_connect(client, userdata, flags, rc):
    """Subscribe on connect."""
    client.subscribe('kgrund/fukt')
    client.subscribe('kgrund/temp')
    client.subscribe('VS1/VS1_GT1')
    client.subscribe('VS1/VS1_GT2')
    client.subscribe('VS1/VS1_GT3')


def on_message(client, userdata, msg):
    """Connect to sql on connect."""
    topic = msg.topic.replace('/', '_')
    payload = float(msg.payload)
    put_sql(topic, payload)


if __name__ == '__main__':
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    engine = create_engine('postgresql://alex:bit@192.168.1.19:5432/alex')
    Session = sessionmaker(bind=engine)
    client.connect_async('192.168.1.19', 1883, 60)
    client.loop_forever()
