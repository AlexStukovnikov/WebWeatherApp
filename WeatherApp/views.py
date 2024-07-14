import datetime

import requests
from django.shortcuts import render

# Create your views here.

def index(request):
    API_KEY = "8d711ac9628db42328723afd600f41d9"
    current_weather_url = "https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}&lang=ru"
    forecast_weather_url = "https://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&units=metric&appid={}&lang=ru"

    if request.method == "POST":
        city = request.POST['city']

        weather_data, daily_forecasts = fetch_weather_and_forecast(city, API_KEY, current_weather_url, forecast_weather_url)

        context = {
            'weather_data': weather_data,
            'daily_forecasts': daily_forecasts
        }

        return render(request, 'weatherapp/index.html', context)

    else:
        return render(request, 'weatherapp/index.html')
    

def fetch_weather_and_forecast(city, api_key, current_weather_url, forecast_weather_url):
    response = requests.get(current_weather_url.format(city, api_key)).json()
    lat, lon = response['coord']['lat'], response['coord']['lon']
    forecast_response = requests.get(forecast_weather_url.format(lat, lon, api_key)).json()

    weather_data = {
        "city": city,
        "temperature": response['main']['temp'],
        "description": response['weather'][0]['description'],
        "icon": response['weather'][0]['icon'],
    }

    daily_forecasts = []
    for daily_data in forecast_response['list'][:8]:
        daily_forecasts.append({
            "day": datetime.datetime.fromtimestamp(daily_data['dt']).strftime('%A'),
            "time": datetime.datetime.fromtimestamp(daily_data['dt']).strftime('%H:%M'),
            "temperature": daily_data['main']['temp'],
            "description": daily_data['weather'][0]['description'],
            "icon": daily_data['weather'][0]['icon'],
        })

    return weather_data, daily_forecasts