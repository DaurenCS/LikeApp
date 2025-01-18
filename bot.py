import requests

# Укажите данные для логина
login_url = "https://auth-wytb.onrender.com/api/v1/login"
token = ""
login_data = {
    "email":"madiyarbek2004@gmail.com",    
    "password": "Diplomka2025!!"  # Ваше имя пользователя
}

# Отправляем запрос на логин
response = requests.post(login_url, json=login_data)

# Проверяем статус ответа
if response.status_code == 200:
    token = response.json().get("data", {}).get("access_token")
    print("Token received:", token)
else:
    print("Error during login:", response.json())

if token:
    # Указываем URL для запроса к профилям противоположного пола
    profiles_url = "https://auth-wytb.onrender.com/api/v1/login/api/v1/refresh"
    
    # Заголовки, включая токен для аутентификации
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Отправляем GET-запрос с заголовками
    response = requests.get(profiles_url, headers=headers)
    
    # Проверяем ответ
    if response.status_code == 200:
        try:
            profiles = response.json()
            print("Profiles:", profiles)
        except requests.exceptions.JSONDecodeError:
            print("Response is not valid JSON. Text:", response.text)
    else:
        print("Error:", response.status_code, response.text)
