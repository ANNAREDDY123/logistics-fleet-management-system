from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date

from database import get_db
from models import Trip, Vehicle, Driver
from schemas import TripCreate, TripResponse
from routes.auth import role_required

router = APIRouter(
    prefix="/trips",
    tags=["Trips"]
)



# CREATE TRIP


@router.post(
    "/",
    response_model=TripResponse
)
def create_trip(
    trip: TripCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        role_required(
            ["Admin", "Fleet Manager"]
        )
    )
):

    vehicle = db.query(
        Vehicle
    ).filter(
        Vehicle.id == trip.vehicle_id
    ).first()

    if not vehicle:

        raise HTTPException(
            status_code=404,
            detail="Vehicle not found."
        )

    if vehicle.status == "Maintenance":

        raise HTTPException(
            status_code=400,
            detail="Vehicle is under maintenance."
        )

    driver = db.query(
        Driver
    ).filter(
        Driver.id == trip.driver_id
    ).first()

    if not driver:

        raise HTTPException(
            status_code=404,
            detail="Driver not found."
        )

    if driver.status == "Inactive":

        raise HTTPException(
            status_code=400,
            detail="Driver is inactive."
        )

    if driver.license_expiry < date.today():

        raise HTTPException(
            status_code=400,
            detail="Driver license has expired."
        )

    active_vehicle_trip = db.query(
        Trip
    ).filter(
        Trip.vehicle_id == trip.vehicle_id,
        Trip.trip_status.in_(
            [
                "Scheduled",
                "Started",
                "In Transit"
            ]
        )
    ).first()

    if active_vehicle_trip:

        raise HTTPException(
            status_code=400,
            detail="Vehicle already has an active trip."
        )

    active_driver_trip = db.query(
        Trip
    ).filter(
        Trip.driver_id == trip.driver_id,
        Trip.trip_status.in_(
            [
                "Scheduled",
                "Started",
                "In Transit"
            ]
        )
    ).first()

    if active_driver_trip:

        raise HTTPException(
            status_code=400,
            detail="Driver already has an active trip."
        )

    new_trip = Trip(
        vehicle_id=trip.vehicle_id,
        driver_id=trip.driver_id,
        source=trip.source,
        destination=trip.destination,
        start_date=trip.start_date,
        expected_delivery_date=trip.expected_delivery_date,
        distance=trip.distance,
        trip_status="Scheduled"
    )

    vehicle.status = "Assigned"

    driver.status = "Assigned"

    db.add(new_trip)

    db.commit()

    db.refresh(new_trip)

    return new_trip
    
# GET ALL TRIPS


@router.get(
    "/",
    response_model=list[TripResponse]
)
def get_all_trips(
    db: Session = Depends(get_db)
):

    return db.query(
        Trip
    ).all()



# GET TRIP BY ID

@router.get(
    "/{trip_id}",
    response_model=TripResponse
)
def get_trip_by_id(
    trip_id: int,
    db: Session = Depends(get_db)
):

    trip = db.query(
        Trip
    ).filter(
        Trip.id == trip_id
    ).first()

    if not trip:

        raise HTTPException(
            status_code=404,
            detail="Trip not found."
        )

    return trip


# START TRIP


@router.put("/{trip_id}/start")
def start_trip(
    trip_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        role_required(
            ["Admin", "Fleet Manager"]
        )
    )
):

    trip = db.query(Trip).filter(
        Trip.id == trip_id
    ).first()

    if not trip:

        raise HTTPException(
            status_code=404,
            detail="Trip not found."
        )

    trip.trip_status = "Started"

    db.commit()

    return {
        "message": "Trip started successfully."
    }



# COMPLETE TRIP


@router.put("/{trip_id}/complete")
def complete_trip(
    trip_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        role_required(
            ["Admin", "Fleet Manager"]
        )
    )
):

    trip = db.query(Trip).filter(
        Trip.id == trip_id
    ).first()

    if not trip:

        raise HTTPException(
            status_code=404,
            detail="Trip not found."
        )

    vehicle = db.query(Vehicle).filter(
        Vehicle.id == trip.vehicle_id
    ).first()

    driver = db.query(Driver).filter(
        Driver.id == trip.driver_id
    ).first()

    trip.trip_status = "Delivered"

    vehicle.status = "Available"

    driver.status = "Active"

    db.commit()

    return {
        "message": "Trip completed successfully."
    }



# CANCEL TRIP


@router.put("/{trip_id}/cancel")
def cancel_trip(
    trip_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        role_required(
            ["Admin", "Fleet Manager"]
        )
    )
):

    trip = db.query(Trip).filter(
        Trip.id == trip_id
    ).first()

    if not trip:

        raise HTTPException(
            status_code=404,
            detail="Trip not found."
        )

    vehicle = db.query(Vehicle).filter(
        Vehicle.id == trip.vehicle_id
    ).first()

    driver = db.query(Driver).filter(
        Driver.id == trip.driver_id
    ).first()

    trip.trip_status = "Cancelled"

    vehicle.status = "Available"

    driver.status = "Active"

    db.commit()

    return {
        "message": "Trip cancelled successfully."
    }

