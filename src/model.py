from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./test.db")
print(DATABASE_URL)
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class StoreModel(Base):
    __tablename__ = "stores"

    id = Column(Integer, primary_key=True, index=True)
    store_name = Column(String, nullable=False)
    store_address = Column(String, nullable=False)

    def as_dict(self):
        return {"id": self.id, "name": self.store_name, "address": self.store_address}


class CarModel(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True, index=True)
    car_name = Column(String, nullable=False)
    car_color = Column(String, nullable=False)
    car_model = Column(String, nullable=False)
    car_price = Column(Float, nullable=False)
    store = Column(String, nullable=False)

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.car_name,
            "model": self.car_model,
            "color": self.car_color,
            "price": self.car_price,
            "store": self.store,
        }