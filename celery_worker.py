# import os
from hamcwebc.app import celery, create_app
from hamcwebc.settings import DevConfig

app = create_app(DevConfig)
app.app_context().push()
