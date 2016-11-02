"""Delay functions with celery."""
from .extensions import celery, db
from .connect_to_socket import call_server
try:
    from .database import Sensor
except ImportError:
    from hamcwebc.database import Sensor


@celery.task(name='example_add')
def add_together(a, b):
    """Test function for celery."""
    return a + b


@celery.task(name='connect_to_pi')
def connect_to_pi(message):
    """Connect to the pi and request or write data."""
    result = call_server(message)
    for key in result.keys():
        db.session.add(Sensor(name=key, value=result[key]['PV']))
    db.session.commit()
