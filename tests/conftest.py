import pytest
import requests

from helpers import (
    create_registered_user,
    delete_user_by_payload,
    delete_user_by_token,
)


@pytest.fixture
def registered_user():
    user = create_registered_user()

    yield user
    delete_user_by_token(user["token"])


@pytest.fixture
def users_to_delete():
    user_payloads = []

    yield user_payloads

    for user_payload in user_payloads:
        delete_user_by_payload(user_payload)

@pytest.fixture(scope="session")
def actual_ingredients():
    """Получает актуальные ID ингредиентов от API Stellar Burgers"""
    # Полный корректный URL эндпоинта ингредиентов Stellar Burgers
    response = requests.get("https://stellarburgers.education-services.ru/api/ingredients")
    response_body = response.json()
    # Извлекаем все _id из ответа сервера
    return [ingredient["_id"] for ingredient in response_body["data"]]

# update conftest
