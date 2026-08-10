from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Boolean,
    Date,
    DateTime,
    ForeignKey
)

from sqlalchemy.orm import relationship

from database import Base

from datetime import datetime



# USER MODEL


class User(Base):

    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    full_name = Column(
        String,
        nullable=False
    )

    email = Column(
        String,
        unique=True,
        nullable=False
    )

    password = Column(
        String,
        nullable=False
    )

    phone = Column(
        String,
        nullable=True
    )

    role = Column(
        String,
        nullable=False
    )

    is_verified = Column(
        Boolean,
        default=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )



# VEHICLE MODEL


class Vehicle(Base):

    __tablename__ = "vehicles"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    vehicle_number = Column(
        String,
        unique=True,
        nullable=False
    )

    vehicle_type = Column(
        String,
        nullable=False
    )

    model = Column(
        String,
        nullable=False
    )

    manufacturing_year = Column(
        Integer,
        nullable=False
    )

    capacity = Column(
        Float,
        nullable=False
    )

    current_km = Column(
        Float,
        default=0
    )

    status = Column(
        String,
        default="Available"
    )

# DRIVER MODEL


class Driver(Base):

    __tablename__ = "drivers"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String,
        nullable=False
    )

    email = Column(
        String,
        unique=True,
        nullable=False
    )

    phone = Column(
        String,
        nullable=False
    )

    license_number = Column(
        String,
        unique=True,
        nullable=False
    )

    license_expiry = Column(
        Date,
        nullable=False
    )

    experience = Column(
        Integer,
        default=0
    )

    status = Column(
        String,
        default="Active"
    )


# TRIP MODEL


class Trip(Base):

    __tablename__ = "trips"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    vehicle_id = Column(
        Integer,
        ForeignKey("vehicles.id")
    )

    driver_id = Column(
        Integer,
        ForeignKey("drivers.id")
    )

    source = Column(
        String,
        nullable=False
    )

    destination = Column(
        String,
        nullable=False
    )

    start_date = Column(
        DateTime,
        nullable=False
    )

    expected_delivery_date = Column(
        DateTime,
        nullable=False
    )

    distance = Column(
        Float,
        nullable=False
    )

    trip_status = Column(
        String,
        default="Scheduled"
    )

    vehicle = relationship(
        "Vehicle"
    )

    driver = relationship(
        "Driver"
    )


# FUEL MODEL


class Fuel(Base):

    __tablename__ = "fuel"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    vehicle_id = Column(
        Integer,
        ForeignKey("vehicles.id")
    )

    trip_id = Column(
        Integer,
        ForeignKey("trips.id")
    )

    fuel_type = Column(
        String,
        nullable=False
    )

    quantity = Column(
        Float,
        nullable=False
    )

    price_per_litre = Column(
        Float,
        nullable=False
    )

    total_cost = Column(
        Float,
        nullable=False
    )

    fuel_date = Column(
        DateTime,
        default=datetime.utcnow
    )

    vehicle = relationship("Vehicle")
    trip = relationship("Trip")



# MAINTENANCE MODEL


class Maintenance(Base):

    __tablename__ = "maintenance"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    vehicle_id = Column(
        Integer,
        ForeignKey("vehicles.id")
    )

    service_type = Column(
        String,
        nullable=False
    )

    service_date = Column(
        DateTime,
        nullable=False
    )

    service_cost = Column(
        Float,
        nullable=False
    )

    current_km = Column(
        Float,
        nullable=False
    )

    description = Column(
        String,
        nullable=True
    )

    status = Column(
        String,
        default="Scheduled"
    )

    vehicle = relationship("Vehicle")


# TRACKING MODEL


class Tracking(Base):

    __tablename__ = "tracking"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    trip_id = Column(
        Integer,
        ForeignKey("trips.id")
    )

    location = Column(
        String,
        nullable=False
    )

    status = Column(
        String,
        nullable=False
    )

    remarks = Column(
        String,
        nullable=True
    )

    timestamp = Column(
        DateTime,
        default=datetime.utcnow
    )

    trip = relationship("Trip")
