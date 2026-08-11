from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from database import get_db

from models import (
    Vehicle,
    Driver,
    Trip,
    Fuel,
    Maintenance
)

from routes.auth import role_required

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get("/")
def dashboard(
    db: Session = Depends(get_db),
    current_user=Depends(
        role_required(
            ["Admin"]
        )
    )
):

    return {

        "total_vehicles":
            db.query(Vehicle).count(),

        "available_vehicles":
            db.query(Vehicle).filter(
                Vehicle.status == "Available"
            ).count(),

        "vehicles_under_maintenance":
            db.query(Vehicle).filter(
                Vehicle.status == "Maintenance"
            ).count(),

        "total_drivers":
            db.query(Driver).count(),

        "active_drivers":
            db.query(Driver).filter(
                Driver.status == "Active"
            ).count(),

        "total_trips":
            db.query(Trip).count(),

        "completed_trips":
            db.query(Trip).filter(
                Trip.trip_status == "Delivered"
            ).count(),

        "cancelled_trips":
            db.query(Trip).filter(
                Trip.trip_status == "Cancelled"
            ).count(),

        "total_fuel_expense":
            db.query(
                func.coalesce(
                    func.sum(
                        Fuel.total_cost
                    ),
                    0
                )
            ).scalar(),

        "total_maintenance_expense":
            db.query(
                func.coalesce(
                    func.sum(
                        Maintenance.service_cost
                    ),
                    0
                )
            ).scalar()
    }
