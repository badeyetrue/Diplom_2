import allure
import requests
from data import TestData


@allure.step("Получить список ингредиентов")
def get_ingredients():
  return requests.get(TestData.INGREDIENTS_URL)


@allure.step("Создать заказ")
def create_order(payload, headers=None):
  return requests.post(TestData.ORDERS_URL, json=payload, headers=headers)


@allure.suite("Тестирование создания заказа")
class TestCreateOrder:

  @allure.title("Успешное создание заказа авторизованным пользователем")
  def test_create_order_with_auth_success(self, create_user):
    user_res, _ = create_user
    token = user_res.json().get("accessToken")
    headers = {"Authorization": token}

    ing_res = get_ingredients()
    ingredients = [item["_id"] for item in ing_res.json()["data"][:2]]
    payload = {"ingredients": ingredients}

    response = create_order(payload, headers=headers)

    assert response.status_code == 200
    assert response.json().get("success") is True
    assert "order" in response.json()

  @allure.title("Успешное создание заказа неавторизованным пользователем")
  def test_create_order_without_auth_success(self):
    ing_res = get_ingredients()
    ingredients = [item["_id"] for item in ing_res.json()["data"][:2]]
    payload = {"ingredients": ingredients}

    response = create_order(payload)

    assert response.status_code == 200
    assert response.json().get("success") is True

  @allure.title("Ошибка при создании заказа без ингредиентов")
  def test_create_order_empty_ingredients_error(self, create_user):
    user_res, _ = create_user
    token = user_res.json().get("accessToken")
    headers = {"Authorization": token}
    payload = {"ingredients": []}

    response = create_order(payload, headers=headers)

    assert response.status_code == 400
    assert response.json().get("success") is False
    assert response.json().get("message") == "Ingredient ids must be provided"

  @allure.title("Ошибка при передаче невалидного ID ингредиента")
  def test_create_order_invalid_ingredients_error(self, create_user):
    user_res, _ = create_user
    token = user_res.json().get("accessToken")
    headers = {"Authorization": token}
    payload = {"ingredients": [TestData.INVALID_INGREDIENT_ID]}

    response = create_order(payload, headers=headers)

    assert response.status_code == 400
    assert response.json().get("success") is False
