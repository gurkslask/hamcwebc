"""Loads the data points configuration from a import JSON file."""
import json
import os

from .extensions import db, celery
from .database import Sensor, SensorLimit


class InitSQL(object):
    """Takes JSON and puts into SQL database."""

    def __init__(self):
        """Constructor."""
        self.file_name = 'data_points.json'
        self.app_dir = os.path.abspath(os.path.dirname(__file__))
        self.a()
        self.update_value()

    def read_file(self):
        """Extract the JSON file."""
        with open(os.path.join(self.app_dir, self.file_name), 'r') as f:
            self.jsonData = json.load(f)
            return self.jsonData

    def make_sql_insert(self, sql_values):
        """Take SQL_values and make an INSERT statement."""
        for i in sql_values:
            limits = [i for i in sql_values[i]['limits']]
            sensorlimits = [SensorLimit(name=i['name'], value=i['value']) for i in limits]
            for limit in sensorlimits:
                if not SensorLimit.query.filter_by(name=limit.name).first():
                    db.session.add(limit)
                else:
                    print('{} Already exists'.format(limit.name))
            if not Sensor.query.filter_by(name=sql_values[i]['name']).first():
                # db.session.add(Sensor(name=sql_values[i]['name'], value=sql_values[i]['value']))
                db.session.add(Sensor(name=sql_values[i]['name'], value=sql_values[i]['value'], limits=sensorlimits))
            else:
                print('{} Already exists'.format(sql_values[i]['name']))
        db.session.commit()

    def a(self):
        """Tie together everything."""
        self.read_file()
        self.make_sql_insert(self.jsonData)

    def update_value(self):
        """Test update function."""
        sensor = Sensor.query.filter_by(name='GT1').first()
        sensor.update(True, value=578)


if __name__ == '__main__':
    a = InitSQL()
    print(a.do_work())
