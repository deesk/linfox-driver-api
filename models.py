#Three Enums that enforce valid domain values -- no bad data gets through
#Three models serving three distinct purposes -- create, update, read
#A computed field that derives truth from data rather than trusting user input

from pydantic import BaseModel, computed_field
from typing import Optional
from datetime import date
from enum import Enum


class LicenceClass(Enum):
    HR = 'HR'
    HC = 'HC'
    MC = 'MC'

class ShiftTypes(Enum):
    DAY = 'day'
    NIGHT = 'night'
    AFTERNOON = 'afternoon'

class RosterPatterns(Enum):
    FIXED = 'fixed'
    ROTATING = 'rotating'
    ON_CALL = 'on_call'

class DriverCreate(BaseModel):
    driver_id: str
    full_name : str
    licence_class: LicenceClass
    licence_expiry: date
    shift_type: ShiftTypes
    roster_pattern: RosterPatterns

class DriverUpdate(BaseModel):
    full_name: Optional[str] = None
    licence_class: Optional[LicenceClass] = None
    licence_expiry: Optional[date] = None
    shift_type: Optional[ShiftTypes] = None
    roster_pattern: Optional[RosterPatterns] = None

class Driver(BaseModel):
    driver_id: str
    full_name : str
    licence_class: LicenceClass
    licence_expiry: date
    shift_type: ShiftTypes
    roster_pattern: RosterPatterns
    is_active: bool
    
    @computed_field
    @property
    def is_licence_expired(self) -> bool:

        return self.licence_expiry < date.today()
