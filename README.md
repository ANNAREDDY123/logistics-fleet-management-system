# logistics-fleet-management-system
A FastAPI-based Logistics &amp; Fleet Management System with JWT Authentication, Role-Based Authorization, Vehicle Management, Driver Management, Trip Management, Fuel Tracking, Maintenance Management, Delivery Tracking, Reports, and PostgreSQL Integration.
# Logistics & Fleet Management System

A backend API system for managing vehicles, drivers, trips, fuel expenses, maintenance records, and real-time trip tracking.

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Pydantic
- JWT Authentication
- Uvicorn
- Swagger / OpenAPI

## Project Structure

```text
logistics-fleet-management-system/
│
├── app/
│   ├── routes/
│   │   ├── auth.py
│   │   ├── vehicles.py
│   │   ├── drivers.py
│   │   ├── trips.py
│   │   ├── fuel.py
│   │   ├── maintenance.py
│   │   ├── tracking.py
│   │   ├── dashboard.py
│   │   └── reports.py
│   │
│   ├── utils/
│   │   └── exceptions.py
│   │
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   └── main.py
│
├── requirements.txt
└── README.md

Features

Authentication
User registration
User login
JWT authentication
Current logged-in user
Role-based access control
Vehicle Management
Create vehicle
Get vehicle by ID
Get all vehicles
Update vehicle
Delete vehicle
Vehicle filtering
Vehicle type filtering
Pagination
Driver Management
Create driver
Get driver by ID
Get all drivers
Update driver
Delete driver
Driver name search
Driver status filtering
Pagination
License expiry validation during trip assignment
Trip Management
Create trip
Get trip by ID
Get all trips
Update trip
Delete trip
Trip status filtering
Source filtering
Destination filtering
Date filtering
Pagination
Start trip
Complete trip
Cancel trip
Fuel Management
Add fuel record
View fuel records
Calculate fuel expense
Fuel expense reporting
Maintenance Management
Add maintenance record
View maintenance records
Track maintenance cost
Update vehicle maintenance status
Trip Tracking
Add tracking records
View tracking history
Automatic tracking when trips are started, completed, or cancelled

Dashboard
Provides:

Total vehicles
Available vehicles
Vehicles under maintenance
Total drivers
Active drivers
Total trips
Completed trips
Cancelled trips
Total fuel expenses
Total maintenance expenses
Reports
Vehicle expense report
Driver trip report
Monthly fuel report
Monthly maintenance report

Validation and Business Rules

Vehicle capacity must be greater than zero.
Trip distance must be greater than zero.
Fuel quantity must be greater than zero.
Fuel price must be greater than zero.
Maintenance cost must be greater than zero.
Inactive drivers cannot be assigned to trips.
Expired driver licenses cannot be assigned to trips.
A vehicle cannot have multiple active trips.
A driver cannot have multiple active trips.
Vehicle and driver statuses are updated automatically during trip lifecycle.
Global exception handling is implemented.

Database

The application uses PostgreSQL with SQLAlchemy ORM.
Database configuration is maintained in the application configuration/database files.

Error Handling
The application provides:

Validation errors
HTTP exceptions
Role-based authorization errors
Global exception handling
Consistent API error responses
