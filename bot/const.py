LOCATION_SEPARATOR = ";"

# Maximum locations allowed in a request
MAX_LOCATIONS_PER_MESSAGE = 10

# Maximum API requests per second (approximately)
# e.g. a rate of 4 means 4 requests/s after exhausting the capacity
# and every 1/4th of a second a token is added
# see https://en.wikipedia.org/wiki/Token_bucket
FETCH_RATE = 4

# Maximum requests made at once (bucket capacity)
FETCH_CAPACITY = 10

# Max attempts to request the weather API
MAX_RETRIES = 5

# Weather API request timeout
REQUEST_TIMEOUT = 10

HELP_TEXT = """
/start, /help - вывод этой команды

место1;...;место1 - получение погоды городов (до 10)
Примеры запросов:
1. Москва
2. Moscow; London; Paris
3. 1;2;3;4;5;6;7;8;9;10;11
4. notfound
5. petersburg,us;виктория,cl;виктория (2-буквенный код страны)

Ответы:
1.
Город: Moscow, RU (Москва)
Температура: 30.96 °C
Скорость ветра: 5.43 м/с

2.
Город: Moscow, RU (Москва)
Температура: 31.15 °C
Скорость ветра: 5.43 м/с

Город: London, GB (Лондон)
Температура: 17.53 °C
Скорость ветра: 0.89 м/с

Город: Paris, FR (Париж)
Температура: 21.13 °C
Скорость ветра: 4.63 м/с

3. Пожалуйста, укажите не более 10 городов

4. Ошибка: место notfound не найдено

5.
Город: Petersburg, US
Температура: 28.81 °C
Скорость ветра: 1.9 м/с

Город: Victoria, CL (Виктория)
Температура: 8.42 °C
Скорость ветра: 2.68 м/с

Город: Victoria, CA (Виктория)
Температура: 15.8 °C
Скорость ветра: 6.17 м/с
"""
