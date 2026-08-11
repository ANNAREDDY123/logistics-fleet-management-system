from fastapi import FastAPI

from database import Base, engine

from routes import auth, vehicles, drivers, trips, fuel


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Logistics & Fleet Management System"
)


app.include_router(auth.router)
app.include_router(vehicles.router)
app.include_router(drivers.router)
app.include_router(trips.router)
app.include_router(fuel.router)


@app.get("/")
def home():

    return {
        "message": "Logistics & Fleet Management System API"
    }
