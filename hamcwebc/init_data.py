"""Loads the data points configuration from a import JSON file."""
import json

from .extensions import db
from .database import Sensor


class InitializeSQL(object):
    """Takes JSON and puts into SQL database."""

    def __init__(self):
        """Constructor."""
        self.file_name = 'data_points.json'

    def read_file(self):
        """Extract the JSON file."""
        with open(self.file_name, 'r') as f:
            self.jsonData = json.load(f)
            return self.jsonData

    def make_sql_insert(self, sql_values):
        """Take SQL_values and make an INSERT statement."""
        for i in sql_values:
            print(i)
            print('INSERT INTO sensor Name: {}, Value: {}'.format(
                sql_values[i]['name'], sql_values[i]['value'])
            )
            for j in sql_values[i]['limits']:
                print(j)

    def do_work(self):
        """Tie together everything."""
        self.read_file()
        self.make_sql_insert(self.jsonData)


if __name__ == '__main__':
    a = InitializeSQL()
    print(a.do_work())
