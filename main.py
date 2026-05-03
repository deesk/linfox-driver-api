from fastapi import FastAPI, HTTPException
from models import Driver, DriverUpdate, DriverCreate
import json
from pathlib import Path

app = FastAPI()

DATA_FILE = Path("drivers.json")

def load_drivers():
    with open(DATA_FILE, 'r') as f:
        drivers = json.load(f)

    return drivers


def save_drivers(new_drivers: list):
    with open(DATA_FILE, 'w') as f: 
        json.dump(new_drivers, f, indent=4)


@app.get("/drivers", response_model=list[Driver])
def get_drivers(
    shift_type: str | None = None,
    roster_pattern: str | None = None,
    licence_class: str | None = None,
):
    drivers = load_drivers()
    if shift_type:
        drivers = [d for d in drivers if d["shift_type"] == shift_type.lower()]
    if roster_pattern:
        drivers = [d for d in drivers if d["roster_pattern"] == roster_pattern.lower()]
    if licence_class:
        drivers = [d for d in drivers if d["licence_class"] == licence_class.upper()]
    return drivers


@app.get("/drivers/{driver_id}", response_model=Driver)
def get_driver(driver_id:str):
    drivers = load_drivers()
    driver_id = driver_id.upper()
    
    for driver in drivers:
        if driver["driver_id"] == driver_id:
            return driver
    
    raise HTTPException(status_code = 404, detail="Driver not found")

     
@app.post("/drivers", response_model=Driver)
def add_driver(new_driver: DriverCreate):
    drivers = load_drivers()
    
    for driver in drivers:
        if driver["driver_id"] == new_driver.driver_id:
            raise HTTPException(status_code = 409, detail="Driver already exists")
        
    new_driver = new_driver.model_dump(mode='json')
    new_driver["is_active"] = True
    drivers.append(new_driver)
    
    save_drivers(drivers)

    return new_driver
    

@app.put("/drivers/{driver_id}", response_model=Driver)
def update_driver(driver_id: str, update: DriverUpdate):
    drivers = load_drivers()
    for driver in drivers:
        if driver["driver_id"] == driver_id:
            driver.update(update.model_dump(exclude_unset=True,mode='json'))
            save_drivers(drivers)
            return driver
    raise HTTPException(status_code=404, detail="Driver not found")


@app.delete("/drivers/{driver_id}")
def delete_driver(driver_id: str):
    drivers = load_drivers()
    for driver in drivers:
        if driver["driver_id"] == driver_id:
            driver["is_active"] = False
            save_drivers(drivers)
            return {"message": f"Driver {driver_id} has been deactivated"}
    raise HTTPException(status_code=404, detail="Driver not found")


