"""Delay functions with celery."""
from .extensions import celery
from .connect_to_socket import call_server
from .database import Sensor


@celery.task(name='example_add')
def add_together(a, b):
    """Test function for celery."""
    return a + b


@celery.task(name='connect_to_pi')
def connect_to_pi(message):
    """Connect to the pi and request or write data."""
    result = call_server(message)
    a = Sensor(name=result.keys(), value=result[result.keys]['PV'])
    print(a)
