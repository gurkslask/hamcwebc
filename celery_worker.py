import os
from hamcwebc.app import register_celery
from hamcwebc.extensions import celery

app = register_celery(os.getenv('FLASK_CONFIG') or 'default')
app.app_context().push()
