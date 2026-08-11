from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from database import get_db

from models import Fuel, Vehicle, Trip

from schemas import FuelCreate, FuelResponse

from routes.auth import role_required


router = APIRouter(
    prefix="/fuel",
    tags=["Fuel"]
)



# ADD FUEL


@router.post(
    "/",
    response_model=FuelResponse
)
def add_fuel(
    fuel: FuelCreate,
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
        Vehicle.id == fuel.vehicle_id
    ).first()

    if not vehicle:

        raise HTTPException(
            status_code=404,
            detail="Vehicle not found."
        )

    trip = db.query(
        Trip
    ).filter(
        Trip.id == fuel.trip_id
    ).first()

    if not trip:

        raise HTTPException(
            status_code=404,
            detail="Trip not found."
        )

    total_cost = (
        fuel.quantity *
        fuel.price_per_litre
    )

    new_fuel = Fuel(
        vehicle_id=fuel.vehicle_id,
        trip_id=fuel.trip_id,
        fuel_type=fuel.fuel_type,
        quantity=fuel.quantity,
        price_per_litre=fuel.price_per_litre,
        total_cost=total_cost,
        fuel_date=datetime.utcnow()
    )

    db.add(new_fuel)

    db.commit()

    db.refresh(new_fuel)

    return new_fuel

# ==========================
# GET ALL FUEL RECORDS
# ==========================

@router.get(
    "/",
    response_model=list[FuelResponse]
)
def get_all_fuel(
    db: Session = Depends(get_db)
):

    return db.query(
        Fuel
    ).all()



# VEHICLE FUEL HISTORY


@router.get(
    "/vehicle/{vehicle_id}",
    response_model=list[FuelResponse]
)
def get_vehicle_fuel_history(
    vehicle_id: int,
    db: Session = Depends(get_db)
):

    vehicle = db.query(
        Vehicle
    ).filter(
        Vehicle.id == vehicle_id
    ).first()

    if not vehicle:

        raise HTTPException(
            status_code=404,
            detail="Vehicle not found."
        )

    return db.query(
        Fuel
    ).filter(
        Fuel.vehicle_id == vehicle_id
    ).all()
