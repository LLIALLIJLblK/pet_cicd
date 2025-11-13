from pydantic import BaseModel
from typing import Optional
from enum import Enum

class PetType(str, Enum):
    CAT = "cat"
    PARROT = "parrot"

class Pet(BaseModel):
    id: int
    name: str
    age: int
    type: PetType
    price: float
    description: Optional[str] = None

class PetCreate(BaseModel):
    name: str
    age: int
    type: PetType
    price: float
    description: Optional[str] = None