from .extensions import celery


@celery.task(name='example_add')
def add_together(a, b):
    return a + b
