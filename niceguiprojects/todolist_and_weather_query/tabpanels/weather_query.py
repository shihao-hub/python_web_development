import random

import requests

from nicegui import ui


# 天气API类
class WeatherAPI:
    def __init__(self):
        self.api_key = "YOUR_API_KEY"  # 替换为实际的API密钥
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"
        self.cities = ['北京', '上海', '广州', '深圳', '杭州', '成都', '武汉', '南京']
        self.weather_data = {}

    def get_weather(self, city):
        if not self.api_key or self.api_key == "YOUR_API_KEY":
            # 模拟数据，如果未设置API密钥
            return self.mock_weather(city)

        try:
            params = {
                'q': city,
                'appid': self.api_key,
                'units': 'metric',
                'lang': 'zh_cn'
            }
            response = requests.get(self.base_url, params=params, timeout=5)
            data = response.json()

            if response.status_code == 200:
                return {
                    'city': city,
                    'temp': data['main']['temp'],
                    'feels_like': data['main']['feels_like'],
                    'humidity': data['main']['humidity'],
                    'description': data['weather'][0]['description'],
                    'icon': data['weather'][0]['icon']
                }
            else:
                return self.mock_weather(city)
        except:
            return self.mock_weather(city)

    def mock_weather(self, city):
        # 生成模拟天气数据
        temps = random.uniform(10, 30)
        descriptions = ['晴天', '多云', '小雨', '局部阵雨', '阴天']
        icons = ['01d', '02d', '03d', '04d', '09d', '10d', '11d', '13d', '50d']

        return {
            'city': city,
            'temp': round(temps, 1),
            'feels_like': round(temps + random.uniform(-2, 2), 1),
            'humidity': random.randint(30, 90),
            'description': random.choice(descriptions),
            'icon': random.choice(icons)
        }

    def get_weather_icon(self, icon_code):
        return f"https://openweathermap.org/img/wn/{icon_code}@2x.png"


# 创建应用实例
weather_api = WeatherAPI()


def weather_query_panel(tab):
    # 天气查询面板
    with ui.tab_panel(tab).classes('p-4') as weather_section:
        # weather_section.id = 'weather-section'

        ui.label('城市天气查询').classes('text-xl font-bold mb-4')

        # 城市选择和刷新
        with ui.row().classes('w-full items-center mb-4'):
            city_select = ui.select(options=weather_api.cities, value='北京').classes('w-48')
            ui.button('查询', icon='search', on_click=lambda: weather_api.get_weather(city_select.value))
            ui.button('刷新全部', icon='refresh',
                      on_click=lambda: [weather_api.get_weather(city) for city in weather_api.cities])
            ui.space()
            ui.button('添加城市', icon='add_location',
                      on_click=lambda: weather_api.cities.append(city_input.value) or city_select.update()).props(
                'outline')
            city_input = ui.input(placeholder='输入新城市...').classes('w-32')

        # 天气卡片网格
        with ui.grid(columns=3).classes('w-full gap-4'):
            for city in weather_api.cities:
                weather = weather_api.get_weather(city)
                with ui.card().classes('p-4 w-full h-48 relative'):
                    with ui.column():
                        ui.label(city).classes('text-lg font-bold')
                        with ui.row().classes('items-center'):
                            ui.image(weather_api.get_weather_icon(weather['icon'])).classes('w-16 h-16')
                            ui.label(f'{weather["temp"]}°C').classes('text-3xl')
                        ui.label(weather['description']).classes('text-lg')
                        with ui.row().classes('w-full justify-between mt-2'):
                            ui.badge(f'体感: {weather["feels_like"]}°C', color='blue')
                            ui.badge(f'湿度: {weather["humidity"]}%', color='teal')

                    ui.button(icon='close', on_click=lambda c=city: weather_api.cities.remove(c) or None) \
                        .props('flat dense').classes('absolute top-2 right-2')
