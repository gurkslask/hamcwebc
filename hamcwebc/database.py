# -*- coding: utf-8 -*-
"""Database module, including the SQLAlchemy database object and DB-related utilities."""
from sqlalchemy.orm import relationship

from .compat import basestring
from .extensions import db


# Alias common SQLAlchemy names
Column = db.Column
relationship = relationship


class CRUDMixin(object):
    """Mixin that adds convenience methods for CRUD (create, read, update, delete) operations."""

    @classmethod
    def create(cls, **kwargs):
        """Create a new record and save it the database."""
        instance = cls(**kwargs)
        return instance.save()

    def update(self, commit=True, **kwargs):
        """Update specific fields of a record."""
        print('here goes update')
        print(kwargs)
        print(commit)
        for attr, value in kwargs.items():
            print(attr, value)
            setattr(self, attr, value)
        return commit and self.save() or self

    def save(self, commit=True):
        """Save the record."""
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def delete(self, commit=True):
        """Remove the record from the database."""
        db.session.delete(self)
        return commit and db.session.commit()


class Model(CRUDMixin, db.Model):
    """Base model class that includes CRUD convenience methods."""

    __abstract__ = True


# From Mike Bayer's "Building the app" talk
# https://speakerdeck.com/zzzeek/building-the-app
class SurrogatePK(object):
    """A mixin that adds a surrogate integer 'primary key' column named ``id`` to any declarative-mapped class."""

    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)

    @classmethod
    def get_by_id(cls, record_id):
        """Get record by ID."""
        if any(
                (isinstance(record_id, basestring) and record_id.isdigit(),
                 isinstance(record_id, (int, float))),
        ):
            return cls.query.get(int(record_id))
        return None


def reference_col(tablename, nullable=False, pk_name='id', **kwargs):
    """Column that adds primary key foreign key reference.

    Usage: ::

        category_id = reference_col('category')
        category = relationship('Category', backref='categories')
    """
    return db.Column(
        db.ForeignKey('{0}.{1}'.format(tablename, pk_name)),
        nullable=nullable, **kwargs)


class Sensor(Model, SurrogatePK):
    """Sensor class that connects to limits, alarm and trends."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    value = db.Column(db.Float)
    limits = db.relationship('SensorLimit', backref='sensors')
    trends_id = db.Column(db.Integer, db.ForeignKey('trend.id'))

    def __init__(self, name, **kwargs):
        """Create instance."""
        db.Model.__init__(self, name=name, **kwargs)

    @property
    def value(self):
        """Return value."""
        return '{}'.format(self.value)

    @property
    def name(self):
        """Return name."""
        return '{}'.format(self.name)

    def __repr__(self):
        """Print data."""
        return 'Name: {}, Value: {}, limits: {}'.format(self.name, self.value, self.limits)


class SensorLimit(CRUDMixin, db.Model):
    """Sensor limits that connects to Sensor."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    value = db.Column(db.Float)
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensor.id'))

    def __repr__(self):
        """Print data."""
        return 'Name: {}, Value: {}, sensor_id: {}'.format(self.name, self.value, self.sensor_id)


class Trend(CRUDMixin, db.Model):
    """Data points (time and value) that connects to Sensor."""

    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Float)
    time = db.Column(db.DateTime)
    sensors = db.relationship('Sensor', backref='trends')

    def __repr__(self):
        """Print data."""
        return 'Name: {}, Value: {}, Time: {},sensor_id: {}'.format(
                self.name, self.value, self.time, self.sensor_id)
