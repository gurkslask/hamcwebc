"""Delay functions with celery."""
from .extensions import celery, db
from .connect_to_socket import read_values
from hamcwebc.user.models import Sensor, SensorTimeData


@celery.task(name='example_add')
def add_together(a, b):
    """Test function for celery."""
    return a + b


@celery.task(name='connect_to_pi')
def connect_to_pi():
    """Connect to the pi and request or write data."""
    result = read_values()
    for key in result.keys():
        sensor = Sensor.query.filter_by(name=key).first()
        pv = result[key]['PV']
        if sensor:
            """If sensor exists."""
            sensortimedata = SensorTimeData()
            sensortimedata.data = pv
            sensor.value = pv
            sensor.timedata = sensor.timedata + [sensortimedata]
            db.session.add(sensortimedata)
            db.session.add(sensor)
        else:
            sensor = Sensor(key)
            sensor.value = pv
            db.session.add(sensor)
    db.session.commit()
