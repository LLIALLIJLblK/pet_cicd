from fastapi import FastAPI
from app.routes import pets, health

app = FastAPI(
    title="Pet Shop API",
    description="API для зоомагазина с котятами и попугаями",
    version="1.0.0"
)

# Подключаем роуты
app.include_router(health.router, prefix="/health", tags=["health"])
app.include_router(pets.router, prefix="/pets", tags=["pets"])

@app.get("/")
async def root():
    return {"message": "Добро пожаловать в зоомагазин!"}