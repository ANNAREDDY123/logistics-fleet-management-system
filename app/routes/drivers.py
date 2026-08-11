from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Driver
from schemas import DriverCreate, DriverResponse
from routes.auth import role_required

router = APIRouter(
    prefix="/drivers",
    tags=["Drivers"]
)


# CREATE DRIVER

@router.post(
    "/",
    response_model=DriverResponse
)
def create_driver(
    driver: DriverCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        role_required(
            ["Admin", "Fleet Manager"]
        )
    )
):

    existing_driver = db.query(
        Driver
    ).filter(
        Driver.license_number == driver.license_number
    ).first()

    if existing_driver:

        raise HTTPException(
            status_code=400,
            detail="License number already exists."
        )

    existing_email = db.query(
        Driver
    ).filter(
        Driver.email == driver.email
    ).first()

    if existing_email:

        raise HTTPException(
            status_code=400,
            detail="Email already exists."
        )

    new_driver = Driver(
        name=driver.name,
        email=driver.email,
        phone=driver.phone,
        license_number=driver.license_number,
        license_expiry=driver.license_expiry,
        experience=driver.experience,
        status=driver.status
    )

    db.add(new_driver)

    db.commit()

    db.refresh(new_driver)

    return new_driver


# ==========================
# GET ALL DRIVERS
# ==========================

@router.get(
    "/",
    response_model=list[DriverResponse]
)
def get_all_drivers(
    name: str = None,
    status: str = None,
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db)
):

    query = db.query(Driver)

    if name:

        query = query.filter(
            Driver.name.ilike(f"%{name}%")
        )

    if status:

        query = query.filter(
            Driver.status == status
        )

    drivers = query.offset(
        (page - 1) * limit
    ).limit(
        limit
    ).all()

    return drivers

# UPDATE DRIVER


@router.put(
    "/{driver_id}",
    response_model=DriverResponse
)
def update_driver(
    driver_id: int,
    updated_driver: DriverCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        role_required(
            ["Admin", "Fleet Manager"]
        )
    )
):

    driver = db.query(
        Driver
    ).filter(
        Driver.id == driver_id
    ).first()

    if not driver:

        raise HTTPException(
            status_code=404,
            detail="Driver not found."
        )

    existing_license = db.query(
        Driver
    ).filter(
        Driver.license_number == updated_driver.license_number,
        Driver.id != driver_id
    ).first()

    if existing_license:

        raise HTTPException(
            status_code=400,
            detail="License number already exists."
        )

    existing_email = db.query(
        Driver
    ).filter(
        Driver.email == updated_driver.email,
        Driver.id != driver_id
    ).first()

    if existing_email:

        raise HTTPException(
            status_code=400,
            detail="Email already exists."
        )

    driver.name = updated_driver.name
    driver.email = updated_driver.email
    driver.phone = updated_driver.phone
    driver.license_number = updated_driver.license_number
    driver.license_expiry = updated_driver.license_expiry
    driver.experience = updated_driver.experience
    driver.status = updated_driver.status

    db.commit()
    db.refresh(driver)

    return driver



# DELETE DRIVER


@router.delete("/{driver_id}")
def delete_driver(
    driver_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        role_required(
            ["Admin"]
        )
    )
):

    driver = db.query(
        Driver
    ).filter(
        Driver.id == driver_id
    ).first()

    if not driver:

        raise HTTPException(
            status_code=404,
            detail="Driver not found."
        )

    db.delete(driver)
    db.commit()

    return {
        "message": "Driver deleted successfully."
    }
