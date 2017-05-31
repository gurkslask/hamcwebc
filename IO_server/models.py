# -*- coding: utf-8 -*-
"""Database module, including the SQLAlchemy database object and DB-related utilities."""

from sqlalchemy import Column, Float, String, DateTime, ForeignKey, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
# from standard_models import CRUDMixin, SurrogatePK, Model

Base = declarative_base()

class Sensor(Base):
    """Sensor class that connects to limits, alarm and trends."""

    __tablename__ = 'sensors'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True)
    value = Column(Float)
    limits = relationship('SensorLimit', backref='sensors')
    timedata = relationship('SensorTimeData', backref='sensors')
    # trends_id = Column(Integer, ForeignKey('trend.id'))

    def __repr__(self):
        """Print data."""
        return 'Name: {}, Value: {}'.format(self.name, self.value)


class SensorLimit(Base):
    """Sensor limits that connects to Sensor."""

    __tablename__ = 'sensorlimits'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    value = Column(Float)
    sensor_id = Column(Integer, ForeignKey('sensors.id'))

    def __repr__(self):
        """Print data."""
        return 'Name: {}, Value: {}, sensor_id: {}'.format(self.name, self.value, self.sensor_id)


class SensorTimeData(Base):
    """Sensor logging with timestamp."""

    __tablename__ = 'sensortimedata'
    id = Column(Integer, primary_key=True)
    data = Column(Float)
    time = Column(DateTime(timezone=True), server_default=func.now())
    sensor_id = Column(Integer, ForeignKey('sensors.id'))

    def __repr__(self):
        """Print data."""
        return 'Data: {}, Time: {}, sensor_id: {}'.format(self.data, self.time, self.sensor_id)


