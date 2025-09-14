import os
import pandas as pd
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from .model import Base, engine, SessionLocal, CarModel, StoreModel

# Crée les tables si elles n'existent pas
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Carshop",
    description="Simple app to expose API for carshop",
    version="1.0.0"
)

# Dépendance pour avoir une session DB par requête
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Initialisation avec les CSV
def reset_db(db: Session):
    db.query(CarModel).delete()
    db.query(StoreModel).delete()
    db.commit()

    # Charger les stores
    stores = pd.read_csv("src/store.csv")
    for _, row in stores.iterrows():
        new_store = StoreModel(store_name=row["store_name"], store_address=row["store_address"])
        db.add(new_store)
    db.commit()

    # Charger les cars
    cars = pd.read_csv("src/cars.csv")
    for _, row in cars.iterrows():
        new_car = CarModel(
            car_name=row["car_name"],
            car_color=row["car_color"],
            car_model=row["car_model"],
            car_price=row["car_price"],
            store=row["store"]
        )
        db.add(new_car)
    db.commit()


@app.on_event("startup")
def startup_event():
    db = SessionLocal()
    reset_db(db)
    db.close()


# Routes FastAPI
@app.get("/")
def get_index():
    return {"Project name": "ShopCars"}


# ---- Cars ----

@app.get("/cars")
def get_cars(db: Session = Depends(get_db)):
    cars = db.query(CarModel).all()
    return {"count": len(cars), "cars": [c.as_dict() for c in cars]}


@app.get("/cars/{car_id}")
def get_car(car_id: int, db: Session = Depends(get_db)):
    car = db.query(CarModel).get(car_id)
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")
    return {"car": car.as_dict()}


@app.post("/cars")
def add_car(car: dict, db: Session = Depends(get_db)):
    try:
        new_car = CarModel(
            car_name=car["name"],
            car_model=car["model"],
            car_color=car["color"],
            car_price=car["price"],
            store=car["store"]
        )
        db.add(new_car)
        db.commit()
        db.refresh(new_car)
        return {"message": "Car added successfully", "car_id": new_car.id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@app.delete("/cars/{car_id}")
def delete_car(car_id: int, db: Session = Depends(get_db)):
    car = db.query(CarModel).get(car_id)
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")
    db.delete(car)
    db.commit()
    return {"message": f"Car with ID {car_id} deleted successfully"}


# ---- Stores ----

@app.get("/stores")
def get_stores(db: Session = Depends(get_db)):
    stores = db.query(StoreModel).all()
    return {"count": len(stores), "stores": [s.as_dict() for s in stores]}


@app.get("/stores/{store_id}")
def get_store(store_id: int, db: Session = Depends(get_db)):
    store = db.query(StoreModel).get(store_id)
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")
    return {"store": store.as_dict()}


@app.post("/stores")
def add_store(store: dict, db: Session = Depends(get_db)):
    try:
        new_store = StoreModel(
            store_name=store["name"],
            store_address=store["address"]
        )
        db.add(new_store)
        db.commit()
        db.refresh(new_store)
        return {"message": "Store added successfully", "store_id": new_store.id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@app.delete("/stores/{store_id}")
def delete_store(store_id: int, db: Session = Depends(get_db)):
    store = db.query(StoreModel).get(store_id)
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")
    db.delete(store)
    db.commit()
    return {"message": f"Store with ID {store_id} deleted successfully"}
