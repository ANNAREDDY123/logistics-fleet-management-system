from pydantic import BaseModel, EmailStr, Field
from datetime import date, datetime
from typing import Optional



# USER


class UserCreate(BaseModel):

    full_name: str

    email: EmailStr

    password: str

    phone: Optional[str] = None

    role: str


class UserResponse(BaseModel):

    id: int

    full_name: str

    email: EmailStr

    phone: Optional[str]

    role: str

    is_verified: bool

    class Config:

        from_attributes = True



# VEHICLE


class VehicleCreate(BaseModel):

    vehicle_number: str

    vehicle_type: str

    model: str

    manufacturing_year: int

    capacity: float = Field(gt=0)

    current_km: float = 0

    status: str = "Available"


class VehicleResponse(VehicleCreate):

    id: int

    class Config:

        from_attributes = True

  
# ==========================
# DRIVER
# ==========================

class DriverCreate(BaseModel):

    name: str

    email: EmailStr

    phone: str

    license_number: str

    license_expiry: date

    experience: int = 0

    status: str = "Active"


class DriverResponse(BaseModel):

    id: int

    name: str

    email: EmailStr

    phone: str

    license_number: str

    license_expiry: date

    experience: int

    status: str

    class Config:

        from_attributes = True

# TRIP


class TripCreate(BaseModel):

    vehicle_id: int

    driver_id: int

    source: str

    destination: str

    start_date: datetime

    expected_delivery_date: datetime

    distance: float = Field(gt=0)


class TripResponse(BaseModel):

    id: int

    vehicle_id: int

    driver_id: int

    source: str

    destination: str

    start_date: datetime

    expected_delivery_date: datetime

    distance: float

    trip_status: str

    class Config:

        from_attributes = True


# FUEL


class FuelCreate(BaseModel):

    vehicle_id: int

    trip_id: int

    fuel_type: str

    quantity: float = Field(gt=0)

    price_per_litre: float = Field(gt=0)


class FuelResponse(BaseModel):

    id: int

    vehicle_id: int

    trip_id: int

    fuel_type: str

    quantity: float

    price_per_litre: float

    total_cost: float

    fuel_date: datetime

    class Config:

        from_attributes = True



# MAINTENANCE


class MaintenanceCreate(BaseModel):

    vehicle_id: int

    service_type: str

    service_date: datetime

    service_cost: float = Field(gt=0)

    current_km: float = Field(ge=0)

    description: Optional[str] = None

    status: str = "Scheduled"


class MaintenanceResponse(MaintenanceCreate):

    id: int

    class Config:

        from_attributes = True



# TRACKING


class TrackingCreate(BaseModel):

    trip_id: int

    location: str

    status: str

    remarks: Optional[str] = None


class TrackingResponse(BaseModel):

    id: int

    trip_id: int

    location: str

    status: str

    remarks: Optional[str]

    timestamp: datetime

    class Config:

        from_attributes = True
