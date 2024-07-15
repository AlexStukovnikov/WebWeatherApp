import datetime
import os
import requests
from django.shortcuts import render

# Create your views here.
API_KEY = os.environ['OPEN_WEATHER_API_KEY']

CURRENT_WEATHER_URL = os.environ['OPEN_CURRENT_WEATHER_URL']
FORECAST_WEATHER_URL = os.environ['OPEN_FORECAST_WEATHER_URL']

def index(request):
    

    if request.method == "POST":
        city = request.POST['city']

        weather_data, daily_forecasts = fetch_weather_and_forecast(city)

        context = {
            'weather_data': weather_data,
            'daily_forecasts': daily_forecasts
        }

        return render(request, 'weatherapp/index.html', context)

    else:
        return render(request, 'weatherapp/index.html')
    

def fetch_weather_and_forecast(city):

    payload = {
        'units': 'metric',
        'appid': API_KEY,
        'lang': 'ru',
        'q': city,
    }
    response = requests.get(CURRENT_WEATHER_URL, payload).json()
    forecast_response = requests.get(FORECAST_WEATHER_URL, payload).json()

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