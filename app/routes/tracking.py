from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from database import get_db

from models import Trip, Tracking

from schemas import TrackingCreate, TrackingResponse

from routes.auth import role_required


router = APIRouter(
    prefix="/trips",
    tags=["Tracking"]
)



# ADD TRACKING

@router.post(
    "/{trip_id}/tracking",
    response_model=TrackingResponse
)
def add_tracking(
    trip_id: int,
    tracking: TrackingCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        role_required(
            ["Admin", "Fleet Manager"]
        )
    )
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

    if trip.trip_status == "Delivered":

        raise HTTPException(
            status_code=400,
            detail="Completed trips cannot receive tracking updates."
        )

    new_tracking = Tracking(
        trip_id=trip_id,
        location=tracking.location,
        status=tracking.status,
        remarks=tracking.remarks,
        timestamp=datetime.utcnow()
    )

    db.add(new_tracking)

    db.commit()

    db.refresh(new_tracking)

    return new_tracking

# GET TRACKING HISTORY


@router.get(
    "/{trip_id}/tracking",
    response_model=list[TrackingResponse]
)
def get_tracking_history(
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

    return db.query(
        Tracking
    ).filter(
        Tracking.trip_id == trip_id
    ).all()
