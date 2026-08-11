from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Vehicle
from schemas import VehicleCreate, VehicleResponse
from routes.auth import role_required

router = APIRouter(
    prefix="/vehicles",
    tags=["Vehicles"]
)


# CREATE VEHICLE

@router.post(
    "/",
    response_model=VehicleResponse
)
def create_vehicle(
    vehicle: VehicleCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        role_required(
            ["Admin", "Fleet Manager"]
        )
    )
):

    existing_vehicle = db.query(
        Vehicle
    ).filter(
        Vehicle.vehicle_number == vehicle.vehicle_number
    ).first()

    if existing_vehicle:

        raise HTTPException(
            status_code=400,
            detail="Vehicle number already exists."
        )

    new_vehicle = Vehicle(
        vehicle_number=vehicle.vehicle_number,
        vehicle_type=vehicle.vehicle_type,
        model=vehicle.model,
        manufacturing_year=vehicle.manufacturing_year,
        capacity=vehicle.capacity,
        current_km=vehicle.current_km,
        status=vehicle.status
    )

    db.add(new_vehicle)

    db.commit()

    db.refresh(new_vehicle)

    return new_vehicle

# GET ALL VEHICLES

@router.get(
    "/",
    response_model=list[VehicleResponse]
)
def get_all_vehicles(
    status: str = None,
    vehicle_type: str = None,
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db)
):

    query = db.query(Vehicle)

    if status:

        query = query.filter(
            Vehicle.status == status
        )

    if vehicle_type:

        query = query.filter(
            Vehicle.vehicle_type == vehicle_type
        )

    vehicles = query.offset(
        (page - 1) * limit
    ).limit(
        limit
    ).all()

    return vehicles
    
# GET VEHICLE BY ID


@router.get(
    "/{vehicle_id}",
    response_model=VehicleResponse
)
def get_vehicle_by_id(
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

    return vehicle

# UPDATE VEHICLE

@router.put(
    "/{vehicle_id}",
    response_model=VehicleResponse
)
def update_vehicle(
    vehicle_id: int,
    updated_vehicle: VehicleCreate,
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
        Vehicle.id == vehicle_id
    ).first()

    if not vehicle:

        raise HTTPException(
            status_code=404,
            detail="Vehicle not found."
        )

    existing_vehicle = db.query(
        Vehicle
    ).filter(
        Vehicle.vehicle_number == updated_vehicle.vehicle_number,
        Vehicle.id != vehicle_id
    ).first()

    if existing_vehicle:

        raise HTTPException(
            status_code=400,
            detail="Vehicle number already exists."
        )

    vehicle.vehicle_number = updated_vehicle.vehicle_number
    vehicle.vehicle_type = updated_vehicle.vehicle_type
    vehicle.model = updated_vehicle.model
    vehicle.manufacturing_year = updated_vehicle.manufacturing_year
    vehicle.capacity = updated_vehicle.capacity
    vehicle.current_km = updated_vehicle.current_km
    vehicle.status = updated_vehicle.status

    db.commit()
    db.refresh(vehicle)

    return vehicle


# DELETE VEHICLE


@router.delete("/{vehicle_id}")
def delete_vehicle(
    vehicle_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        role_required(
            ["Admin"]
        )
    )
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

    db.delete(vehicle)
    db.commit()

    return {
        "message": "Vehicle deleted successfully."
    }
