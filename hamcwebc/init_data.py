"""Loads the data points configuration from a import JSON file."""
import json
import os

from .extensions import db
from .database import Sensor, SensorLimit


class InitSQL(object):
    """Takes JSON and puts into SQL database."""

    def __init__(self):
        """Constructor."""
        self.file_name = 'data_points.json'
        self.app_dir = os.path.abspath(os.path.dirname(__file__))

    def read_file(self):
        """Extract the JSON file."""
        with open(os.path.join(self.app_dir, self.file_name), 'r') as f:
            self.jsonData = json.load(f)
            return self.jsonData

    def make_sql_insert(self, sql_values):
        """Take SQL_values and make an INSERT statement."""
        for i in sql_values:
            for j in sql_values[i]['limits']:
                if not SensorLimit.query.filter_by(name=[j]['name']).first():
                    db.session.add(SensorLimit(
                        name=[j]['name'],
                        value=[j]['value']
                        )
                    )
                else:
                    print('{} Already exists'.format(name=[j]['name']))
                print(j)
            print(Sensor.query.filter_by(name=sql_values[i]['name']).first())
            if not Sensor.query.filter_by(name=sql_values[i]['name']).first():
                db.session.add(Sensor(name=sql_values[i]['name'], value=sql_values[i]['value']))
                db.session.commit()
            else:
                print('{} Already exists'.format(sql_values[i]['name']))

    def do_work(self):
        """Tie together everything."""
        self.read_file()
        self.make_sql_insert(self.jsonData)


if __name__ == '__main__':
    a = InitSQL()
    print(a.do_work())
