class TestData:
    BASE_URL = "https://stellarburgers.education-services.ru"
    
    # Эндпоинты
    CREATE_USER_URL = f"{BASE_URL}/api/auth/register"
    LOGIN_USER_URL = f"{BASE_URL}/api/auth/login"
    USER_URL = f"{BASE_URL}/api/auth/user"
    ORDERS_URL = f"{BASE_URL}/api/orders"
    INGREDIENTS_URL = f"{BASE_URL}/api/ingredients"

    # Невалидные данные
    WRONG_EMAIL = "altai_fail_test_badeyetrue@yandex.ru"
    WRONG_PASSWORD = "wrong_password_123"
    INVALID_INGREDIENT_ID = "61c0c5b71d1f82001bda5123"
