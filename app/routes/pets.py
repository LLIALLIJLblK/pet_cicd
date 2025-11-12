from fastapi import APIRouter, HTTPException
from app.models import Pet, PetCreate, PetType
from typing import List

router = APIRouter()

# In-memory "база данных"
pets_db = [
    Pet(id=1, name="Мурзик", age=2, type=PetType.CAT, price=100.0, description="Ласковый котенок"),
    Pet(id=2, name="Кеша", age=1, type=PetType.PARROT, price=150.0, description="Говорящий попугай"),
    Pet(id=3, name="Барсик", age=3, type=PetType.CAT, price=120.0, description="Игривый кот"),
    Pet(id=4, name="Гоша", age=2, type=PetType.PARROT, price=200.0, description="Яркий попугай ара"),
]

@router.get("/", response_model=List[Pet])
async def get_all_pets():
    return pets_db

@router.get("/{pet_id}", response_model=Pet)
async def get_pet(pet_id: int):
    pet = next((pet for pet in pets_db if pet.id == pet_id), None)
    if not pet:
        raise HTTPException(status_code=404, detail="Питомец не найден")
    return pet

@router.get("/type/{pet_type}", response_model=List[Pet])
async def get_pets_by_type(pet_type: PetType):
    return [pet for pet in pets_db if pet.type == pet_type]

@router.post("/", response_model=Pet)
async def create_pet(pet_create: PetCreate):
    new_id = max(pet.id for pet in pets_db) + 1 if pets_db else 1
    new_pet = Pet(id=new_id, **pet_create.dict())
    pets_db.append(new_pet)
    return new_pet

@router.put("/{pet_id}", response_model=Pet)
async def update_pet(pet_id: int, pet_update: PetCreate):
    pet_index = next((index for index, pet in enumerate(pets_db) if pet.id == pet_id), None)
    if pet_index is None:
        raise HTTPException(status_code=404, detail="Питомец не найден")
    
    updated_pet = Pet(id=pet_id, **pet_update.dict())
    pets_db[pet_index] = updated_pet
    return updated_pet

@router.delete("/{pet_id}")
async def delete_pet(pet_id: int):
    pet_index = next((index for index, pet in enumerate(pets_db) if pet.id == pet_id), None)
    if pet_index is None:
        raise HTTPException(status_code=404, detail="Питомец не найден")
    
    deleted_pet = pets_db.pop(pet_index)
    return {"message": f"Питомец {deleted_pet.name} удален"}