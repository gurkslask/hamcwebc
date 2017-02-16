"""Delay functions with celery."""
from .extensions import celery, db
from .connect_to_socket import read_values
try:
    from .database import Sensor
except ImportError:
    from hamcwebc.database import Sensor


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
        if sensor:
            print(sensor)
            sensor.value = result[key]['PV']
            db.session.add(sensor)
    db.session.commit()
