
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestPetsAPI:
    def test_get_all_pets(self):
        response = client.get("/pets/")
        assert response.status_code == 200
        pets = response.json()
        assert len(pets) > 0
        assert all("name" in pet for pet in pets)

    def test_get_pet_by_id(self):
        response = client.get("/pets/1")
        assert response.status_code == 200
        pet = response.json()
        assert pet["id"] == 1
        assert "name" in pet

    def test_get_pet_not_found(self):
        response = client.get("/pets/999")
        assert response.status_code == 404

    def test_get_pets_by_type_cats(self):
        response = client.get("/pets/type/cat")
        assert response.status_code == 200
        cats = response.json()
        assert all(pet["type"] == "cat" for pet in cats)

    def test_get_pets_by_type_parrots(self):
        response = client.get("/pets/type/parrot")
        assert response.status_code == 200
        parrots = response.json()
        assert all(pet["type"] == "parrot" for pet in parrots)

    def test_create_pet(self):
        new_pet = {
            "name": "Тестовый кот",
            "age": 1,
            "type": "cat",
            "price": 100.0,
            "description": "Тестовое описание"
        }
        response = client.post("/pets/", json=new_pet)
        assert response.status_code == 200
        created_pet = response.json()
        assert created_pet["name"] == "Тестовый кот"
        assert created_pet["id"] is not None

    def test_update_pet(self):
        update_data = {
            "name": "Обновленное имя",
            "age": 4,
            "type": "cat",
            "price": 150.0,
            "description": "Обновленное описание"
        }
        response = client.put("/pets/1", json=update_data)
        assert response.status_code == 200
        updated_pet = response.json()
        assert updated_pet["name"] == "Обновленное имя"
        assert updated_pet["age"] == 4

    def test_update_pet_not_found(self):
        update_data = {
            "name": "Обновленное имя",
            "age": 4,
            "type": "cat",
            "price": 150.0
        }
        response = client.put("/pets/999", json=update_data)
        assert response.status_code == 404

    def test_delete_pet(self):
        # Сначала создаем питомца для удаления
        new_pet = {
            "name": "Для удаления",
            "age": 1,
            "type": "parrot",
            "price": 50.0
        }
        create_response = client.post("/pets/", json=new_pet)
        pet_id = create_response.json()["id"]

        # Затем удаляем его
        delete_response = client.delete(f"/pets/{pet_id}")
        assert delete_response.status_code == 200

        # Проверяем, что питомец действительно удален
        get_response = client.get(f"/pets/{pet_id}")
        assert get_response.status_code == 404

    def test_delete_pet_not_found(self):
        response = client.delete("/pets/999")
        assert response.status_code == 404