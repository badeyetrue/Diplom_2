import requests
import allure
from data import TestData

@allure.suite("Тестирование создания заказа")
class TestCreateOrder:
    
    @allure.title("Успешное создание заказа авторизованным пользователем")
    def test_create_order_with_auth_success(self, create_user):
        user_res, _ = create_user
        token = user_res.json().get("accessToken")
        headers = {"Authorization": token}
        
        ing_res = requests.get(TestData.INGREDIENTS_URL)
        ingredients = [item["_id"] for item in ing_res.json()["data"][:2]]
        
        payload = {"ingredients": ingredients}
        response = requests.post(TestData.ORDERS_URL, json=payload, headers=headers)
        
        assert response.status_code == 200
        assert response.json().get("success") is True
        assert "order" in response.json()

    @allure.title("Успешное создание заказа неавторизованным пользователем")
    def test_create_order_without_auth_success(self):
        ing_res = requests.get(TestData.INGREDIENTS_URL)
        ingredients = [item["_id"] for item in ing_res.json()["data"][:2]]
        
        payload = {"ingredients": ingredients}
        response = requests.post(TestData.ORDERS_URL, json=payload)
        
        assert response.status_code == 200
        assert response.json().get("success") is True

    @allure.title("Ошибка при создании заказа без ингредиентов")
    def test_create_order_empty_ingredients_error(self, create_user):
        user_res, _ = create_user
        token = user_res.json().get("accessToken")
        headers = {"Authorization": token}
        
        payload = {"ingredients": []}
        response = requests.post(TestData.ORDERS_URL, json=payload, headers=headers)
        
        assert response.status_code == 400
        assert response.json().get("success") is False
        assert response.json().get("message") == "Ingredient ids must be provided"

    @allure.title("Ошибка при передаче невалидного ID ингредиента")
    def test_create_order_invalid_ingredients_error(self, create_user):
        user_res, _ = create_user
        token = user_res.json().get("accessToken")
        headers = {"Authorization": token}
    
        payload = {"ingredients": [TestData.INVALID_INGREDIENT_ID]}
        response = requests.post(TestData.ORDERS_URL, json=payload, headers=headers)
    
        # Сервер возвращает 400 Bad Request на кривой ID ингредиента
        assert response.status_code == 400
        assert response.json().get("success") is False

