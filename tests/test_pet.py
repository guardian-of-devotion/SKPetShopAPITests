import allure
import jsonschema
import requests
from .schemas.pet_schema import PET_SCHEMA

BASE_URL = "http://5.181.109.28:9090/api/v3"

@allure.feature("Pet")
class TestPet:
    @allure.title("Попытка удалить несуществующего питомца")
    def test_delete_nonexistent_pet(self):
        with allure.step("Отправка запроса на удаление несуществующего питомца"):
             response = requests.delete(url = f"{BASE_URL}/pet/9999")

        with allure.step("Проверка статуса ответа"):
             assert response.status_code == 200, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка текстового содержимого ответа"):
            assert response.text == "Pet deleted", "Текст ошибки не совпал с ожидаемым"


    @allure.title("Попытка обновить несуществующего питомца")
    def test_update_nonexistent_pet(self):
        payload = {
            "id": 9999,
            "name": "Non-existent pet",
            "status": "available",
        }
        with allure.step("Отправка запроса на обновление несуществующего питомца"):
            response = requests.put(url = f"{BASE_URL}/pet", json=payload)

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка текстового содержимого ответа"):
            assert response.text == "Pet not found", "Текст ошибки не совпал с ожидаемым"

    @allure.title("Попытка получить информацию о несуществующем питомце")
    def test_get_nonexistent_pet(self):

        with allure.step("Отправка запроса на получение несуществующего питомца"):
            response = requests.get(url = f"{BASE_URL}/pet/9999")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка текстового содержимого ответа"):
            assert response.text == "Pet not found", "Текст ошибки не совпал с ожидаемым"


    @allure.title("Добавление нового питомца")
    def test_create_new_pet(self):
        with allure.step("Подготовка данных для создания питомца"):
            payload = {
            "id": 1,
            "name": "Buddy",
            "status": "available",
            }
        with allure.step("Отправка запроса на добавление нового питомца"):
            response = requests.post(url = f"{BASE_URL}/pet/", json=payload)
            response_json = response.json()

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"
            jsonschema.validate(response_json, PET_SCHEMA)

        with allure.step("Проверка параметров питомца в ответе"):
            assert response_json['id'] == payload['id'], "ID питомца не совпадает с ожидаемым"
            assert response_json['name'] == payload['name'], "Имя питомца не совпадает с ожидаемым"
            assert response_json['status'] == payload['status'], "Статус питомца не совпадает с ожидаемым"

    @allure.title("Добавление нового питомца с полными данными")
    def test_create_new_pet_full(self):
        payload = {
            "id": 5,
            "name": "doggie",
            "category": {
                "id": 1,
                "name": "Dogs",
            },
            "photoUrls": ["string"],
            "tags": [{
                "id": 0,
                "name": "string"
            }],
            "status": "available",
        }
        with allure.step("Отправка запроса на добавление нового питомца с полными данными"):
            response = requests.post(url = f"{BASE_URL}/pet/", json=payload)
            response_json = response.json()

        with allure.step("Проверка статуса ответа:"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"
            jsonschema.validate(response_json, PET_SCHEMA)

        with allure.step("Проверка параметров питомца в ответе"):
            for key in ['id', 'name', 'status', 'photoUrls']:
                assert response_json[key] == payload[key]

            if 'category' in payload:
                assert response_json.get("category") == payload["category"], f"Значение параметров не совпало с ожидаемыми"

            if 'tags' in payload:
                for resp_tag, payload_tag in zip(response_json.get('tags', []), payload.get('tags', [])):
                    if isinstance(payload_tag, dict) and isinstance(resp_tag, dict):
                        for key, value in payload_tag.items():
                            assert resp_tag[key] == value, f"Значение параметра '{key}' не совпало с ожидаемым"