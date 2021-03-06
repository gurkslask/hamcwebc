# -*- coding: utf-8 -*-
"""User models."""
import datetime as dt

from flask_login import UserMixin

from sqlalchemy.sql import func

from hamcwebc.database import Column, Model, SurrogatePK, db, reference_col, relationship, CRUDMixin
from hamcwebc.extensions import bcrypt


class Role(SurrogatePK, Model):
    """A role for a user."""

    __tablename__ = 'roles'
    name = Column(db.String(80), unique=True, nullable=False)
    user_id = reference_col('users', nullable=True)
    user = relationship('User', backref='roles')

    def __init__(self, name, **kwargs):
        """Create instance."""
        db.Model.__init__(self, name=name, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<Role({name})>'.format(name=self.name)


class User(UserMixin, SurrogatePK, Model):
    """A user of the app."""

    __tablename__ = 'users'
    username = Column(db.String(80), unique=True, nullable=False)
    email = Column(db.String(80), unique=True, nullable=False)
    #: The hashed password
    password = Column(db.String(128), nullable=True)
    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    first_name = Column(db.String(30), nullable=True)
    last_name = Column(db.String(30), nullable=True)
    active = Column(db.Boolean(), default=False)
    is_admin = Column(db.Boolean(), default=False)

    def __init__(self, username, email, password=None, **kwargs):
        """Create instance."""
        db.Model.__init__(self, username=username, email=email, **kwargs)
        if password:
            self.set_password(password)
        else:
            self.password = None

    def set_password(self, password):
        """Set password."""
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, value):
        """Check password."""
        return bcrypt.check_password_hash(self.password, value)

    @property
    def full_name(self):
        """Full user name."""
        return '{0} {1}'.format(self.first_name, self.last_name)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<User({username!r})>'.format(username=self.username)


class Sensor(SurrogatePK, Model, CRUDMixin):
    """Sensor class that connects to limits, alarm and trends."""

    __tablename__ = 'sensors'
    name = Column(db.String(80), unique=True)
    value = Column(db.Float)
    limits = db.relationship('SensorLimit', backref='sensors')
    timedata = db.relationship('SensorTimeData', backref='sensors')
    # trends_id = db.Column(db.Integer, db.ForeignKey('trend.id'))

    def __init__(self, name, **kwargs):
        """Create instance."""
        db.Model.__init__(self, name=name, **kwargs)

    def __repr__(self):
        """Print data."""
        return 'Name: {}, Value: {}'.format(self.name, self.value)


class SensorLimit(SurrogatePK, Model, CRUDMixin):
    """Sensor limits that connects to Sensor."""

    __tablename__ = 'sensorlimits'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    value = db.Column(db.Float)
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensors.id'))

    def __repr__(self):
        """Print data."""
        return 'Name: {}, Value: {}, sensor_id: {}'.format(self.name, self.value, self.sensor_id)


class SensorTimeData(SurrogatePK, Model, CRUDMixin):
    """Sensor logging with timestamp."""

    __tablename__ = 'sensortimedata'
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Float)
    time = db.Column(db.DateTime(timezone=True), server_default=func.now())
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensors.id'))

    def __repr__(self):
        """Print data."""
        return 'Data: {}, Time: {}, sensor_id: {}'.format(self.data, self.time, self.sensor_id)
