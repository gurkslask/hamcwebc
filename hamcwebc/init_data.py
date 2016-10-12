"""Loads the data points configuration from a import JSON file."""
import json


class InitializeSQL(object):
    """Takes JSON and puts into SQL database."""

    def __init__(self):
        """Constructor."""
        self.file_name = 'data_points.json'

    @staticmethod
    def read_file(self):
        """Extract the JSON file."""
        with open(self.file_name, 'r') as f:
            self.jsonData = json.load(f)
            return self.jsonData

    def make_sql_insert(self, sql_values):
        """Take SQL_values and make an INSERT statement."""
        for i in sql_values:
            print(i)
        pass

    @staticmethod
    def do_work(self):
        """Tie together everything."""
        self.read_file()
        self.make_sql_insert(self.jsonData)


if __name__ == '__main__':
    a = InitializeSQL()
    print(a.do_work(a))
