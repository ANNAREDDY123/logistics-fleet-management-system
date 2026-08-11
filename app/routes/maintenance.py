from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Maintenance, Vehicle
from schemas import MaintenanceCreate, MaintenanceResponse
from routes.auth import role_required

router = APIRouter(
    prefix="/maintenance",
    tags=["Maintenance"]
)



# CREATE MAINTENANCE


@router.post(
    "/",
    response_model=MaintenanceResponse
)
def create_maintenance(
    maintenance: MaintenanceCreate,
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
        Vehicle.id == maintenance.vehicle_id
    ).first()

    if not vehicle:

        raise HTTPException(
            status_code=404,
            detail="Vehicle not found."
        )

    new_maintenance = Maintenance(
        vehicle_id=maintenance.vehicle_id,
        service_type=maintenance.service_type,
        service_date=maintenance.service_date,
        service_cost=maintenance.service_cost,
        current_km=maintenance.current_km,
        description=maintenance.description,
        status=maintenance.status
    )

    if maintenance.status == "In Progress":

        vehicle.status = "Maintenance"

    db.add(new_maintenance)

    db.commit()

    db.refresh(new_maintenance)

    return new_maintenance


# GET ALL MAINTENANCE


@router.get(
    "/",
    response_model=list[MaintenanceResponse]
)
def get_all_maintenance(
    db: Session = Depends(get_db)
):

    return db.query(
        Maintenance
    ).all()



# GET VEHICLE MAINTENANCE HISTORY


@router.get(
    "/vehicle/{vehicle_id}",
    response_model=list[MaintenanceResponse]
)
def get_vehicle_maintenance_history(
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
        Maintenance
    ).filter(
        Maintenance.vehicle_id == vehicle_id
    ).all()


# UPDATE MAINTENANCE


@router.put(
    "/{maintenance_id}",
    response_model=MaintenanceResponse
)
def update_maintenance(
    maintenance_id: int,
    updated_maintenance: MaintenanceCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        role_required(
            ["Admin", "Fleet Manager"]
        )
    )
):

    maintenance = db.query(
        Maintenance
    ).filter(
        Maintenance.id == maintenance_id
    ).first()

    if not maintenance:

        raise HTTPException(
            status_code=404,
            detail="Maintenance record not found."
        )

    vehicle = db.query(
        Vehicle
    ).filter(
        Vehicle.id == maintenance.vehicle_id
    ).first()

    maintenance.service_type = updated_maintenance.service_type
    maintenance.service_date = updated_maintenance.service_date
    maintenance.service_cost = updated_maintenance.service_cost
    maintenance.current_km = updated_maintenance.current_km
    maintenance.description = updated_maintenance.description
    maintenance.status = updated_maintenance.status

    if updated_maintenance.status == "In Progress":

        vehicle.status = "Maintenance"

    elif updated_maintenance.status == "Completed":

        vehicle.status = "Available"

    db.commit()

    db.refresh(maintenance)

    return maintenance
