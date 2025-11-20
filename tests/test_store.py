import allure
import jsonschema
import pytest
import requests

from store_schema import STORE_SCHEMA

BASE_URL = "http://5.181.109.28:9090/api/v3"


@allure.feature("Store")
class TestStore:
    @allure.title("Размещение заказа")
    def test_create_order(self, create_order):
        with allure.step("Получение ID заказа"):
            order_id = create_order["id"]

        with allure.step("Отправка запроса на получение информации о заказе"):
            response = requests.get(url=f"{BASE_URL}/store/order/{order_id}")

        with allure.step("Проверка статуса ответа и содержимого ответа"):
            assert response.status_code == 200, "Код статуса не совпадает с ожидаемым"
            assert response.json(), "Содержимое ответа не совпадает с ожидаемым"

    @allure.title("Получение информации о заказе по ID")
    def test_get_order(self):
        with allure.step("Отправка запроса на получение информации о заказе"):
            response = requests.get(url=f"{BASE_URL}/store/order/1")

        with allure.step("Проверка статуса ответа и содержимого ответа"):
            assert response.status_code == 200, "Код статуса не совпадает с ожидаемым"
            assert response.json(), "Содержимое ответа не совпадает с ожидаемым"

    @allure.title("Удаление заказа по ID")
    def test_delete_order(self):
        with allure.step("Отправка запроса на удаление заказа по ID"):
            response = requests.delete(url=f"{BASE_URL}/store/order/1")

        with allure.step("Проверка статуса ответа и содержимого ответа"):
            assert response.status_code == 200, "Код статуса не совпадает с ожидаемым"

        with allure.step("Отправка запроса на получение информации о заказе"):
            response = requests.get(url=f"{BASE_URL}/store/order/1")

        with allure.step("Проверка статуса ответа и содержимого ответа"):
            assert response.status_code == 404, "Код статуса не совпадает с ожидаемым"

    @allure.title("Попытка получить информацию о несуществующем заказе")
    def test_get_nonexistent_order(self):
        with allure.step("Отправка запроса на получение информации о несуществующем заказе"):
            response = requests.get(url=f"{BASE_URL}/store/order/9999")

        with allure.step("Проверка статуса ответа и содержимого ответа"):
            assert response.status_code == 404, "Код статуса не совпадает с ожидаемым"
            assert response.text == "Order not found", "Текст ответа не совпадает с ожидаемым"

    @allure.title("Получение инвентаря магазина")
    def test_get_store_inventory(self):
        with allure.step("Отправка запроса на получение магазина инвентаря"):
            response = requests.get(url=f"{BASE_URL}/store/inventory")
            response_json = response.json()

        with allure.step("Проверка статуса ответа и содержимого ответа"):
            assert response.status_code == 200, "Код статуса не совпадает с ожидаемым"
            jsonschema.validate(response_json, STORE_SCHEMA)
            print(response_json)
