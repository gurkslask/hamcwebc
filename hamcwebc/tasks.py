"""Delay functions with celery."""
from .extensions import celery
from .connect_to_socket import call_server


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    """Add periodic tasks to celery."""
    sender.add_periodic_task(5.0, add_together.s(), name='test')


@celery.task(name='example_add')
def add_together(a, b):
    """Test function for celery."""
    return a + b


@celery.task(name='connect_to_pi')
def connect_to_pi(message):
    """Connect to the pi and request or write data."""
    return(call_server(message))
