import requests


class WeatherClient():
    """
    Выполняет запрос на получение текущей погоды для города
    """
    api_key = '99ba78ee79a2a24bc507362c5288a81b'

    def __init__(self):
        """
        Инициализирует класс
        """
        self.session = requests.Session()

    def get_weather_url(self, city):
        """
        Генерирует url включая в него необходимые параметры
        Args:
            city: Город
        Returns:

        """
        url = f'https://api.openweathermap.org/data/2.5/weather?' \
              f'units=metric' \
              f'&q={city}' \
              f'&appid={self.api_key}'
        return url

    def get_weather(self, city):
        """
        Делает запрос на получение погоды
        Args:
            city: Город
        Returns:

        """
        url = self.get_weather_url(city)
        r = self.session.get(url)
        if r.status_code != 200:
            return None
        try:
            data = r.json()
        except ValueError:
            return None

        if not data.get("main"):
            return None

        if not data["main"].get("temp"):
            return None

        return data['main']['temp']

    def city_exists(self, city):
        """
        Делает проверку существования города города
        Args:
            city: Город
        Returns:

        """
        url = self.get_weather_url(city)
        r = self.session.get(url)

        return r.status_code == 200
