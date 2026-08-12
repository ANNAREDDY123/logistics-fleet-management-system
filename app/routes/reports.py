from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from database import get_db

from models import (
    Fuel,
    Maintenance,
    Trip
)

from routes.auth import role_required

router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)



# VEHICLE EXPENSE REPORT


@router.get("/vehicle-expense")
def vehicle_expense_report(
    db: Session = Depends(get_db),
    current_user=Depends(role_required(["Admin"]))
):

    fuel_expense = db.query(
        func.coalesce(func.sum(Fuel.total_cost), 0)
    ).scalar()

    maintenance_expense = db.query(
        func.coalesce(func.sum(Maintenance.service_cost), 0)
    ).scalar()

    return {
        "total_fuel_expense": fuel_expense,
        "total_maintenance_expense": maintenance_expense,
        "total_vehicle_expense": fuel_expense + maintenance_expense
    }




# DRIVER TRIP REPORT


@router.get("/driver-trips")
def driver_trip_report(
    db: Session = Depends(get_db),
    current_user=Depends(role_required(["Admin"]))
):

    report = db.query(
        Trip.driver_id,
        func.count(Trip.id).label("total_trips")
    ).group_by(
        Trip.driver_id
    ).all()

    return [
        {
            "driver_id": row.driver_id,
            "total_trips": row.total_trips
        }
        for row in report
    ]




# MONTHLY FUEL REPORT


@router.get("/monthly-fuel")
def monthly_fuel_report(
    db: Session = Depends(get_db),
    current_user=Depends(role_required(["Admin"]))
):

    report = db.query(
        func.strftime("%Y-%m", Fuel.fuel_date).label("month"),
        func.sum(Fuel.total_cost).label("expense")
    ).group_by(
        func.strftime("%Y-%m", Fuel.fuel_date)
    ).all()

    return [
        {
            "month": row.month,
            "expense": row.expense
        }
        for row in report
    ]


# MONTHLY MAINTENANCE REPORT


@router.get("/monthly-maintenance")
def monthly_maintenance_report(
    db: Session = Depends(get_db),
    current_user=Depends(role_required(["Admin"]))
):

    report = db.query(
        func.strftime("%Y-%m", Maintenance.service_date).label("month"),
        func.sum(Maintenance.service_cost).label("expense")
    ).group_by(
        func.strftime("%Y-%m", Maintenance.service_date)
    ).all()

    return [
        {
            "month": row.month,
            "expense": row.expense
        }
        for row in report
    ]
