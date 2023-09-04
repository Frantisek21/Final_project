
from flask import Flask, render_template, request
import requests
from geopy.geocoders import Nominatim

app = Flask(__name__)
geolocator = Nominatim(user_agent="Project_WeatherApp")

def get_clothing_recommendations(temperature, weather_condition):
    clothing = []
    
    if temperature < -10:
        clothing.extend(["Super heavy winter jacket", "Thermal layers", "Ice skates", "Winter hat", "Gloves", "Thermal Leggings"])
    elif temperature < 0:
        clothing.extend(["Winter coat", "Warm hoodie", "Winter boots", "Hat", "Gloves", "Ear Muffs"])
    elif temperature < 10:
        clothing.extend(["Jacket", "Sweater", "Long-sleeve shirt", "Jeans", "Long socks", "Scarf"])
    elif temperature < 20:
        clothing.extend(["Light jacket", "T-shirt", "Jeans", "Sneakers", "Windbreaker"])
    else:
        clothing.extend(["T-shirt", "Shorts", "Sandals", "Sweat-wicking Shirt", "Breathable Underwear"])

    if weather_condition == "Clear" and temperature >= 20:
        clothing.extend(["Sunglasses", "Sunscreen", "UV Protection Hat"])
    elif weather_condition == "Rain":
        clothing.extend(["Raincoat", "Umbrella", "Waterproof Boots", "Waterproof Pants"])
    elif weather_condition == "Snow":
        clothing.append("Gaiters")

    return clothing

def get_activity_recommendations(temperature, weather_condition):
    activities = []
    
    if weather_condition == "Clear":
        if temperature >= 25:
            activities.extend(["Beach Volleyball", "Surfing", "Sailing", "Kite Flying"])
        elif 15 <= temperature < 25:
            activities.extend(["Tennis", "Skateboarding", "Badminton"])
        elif 10 <= temperature < 15:
            activities.extend(["Mountain Biking", "Trail Running", "Fishing", "Hiking", "Archery"])
    if weather_condition == "Rain":
        activities.extend(["Indoor Basketball", "Indoor Climbing", "Table Tennis"])
    if weather_condition == "Snow" and temperature < 0:
        activities.append("Snowboarding")
    if weather_condition == "Snow" and temperature < -5:
        activities.append("Skiing")
    if temperature < 0 and weather_condition != "Snow":
        activities.append("Ice Skating")
    if weather_condition == "Snow" and -5 <= temperature < 0:
        activities.append("Snowball Fight")
    if not activities:
        activities.append("Yoga") 

    return activities

def get_wikipedia_url(city):
    url = f"https://en.wikipedia.org/w/api.php?action=opensearch&search={city}&limit=1&format=json"
    response = requests.get(url)
    data = response.json()
    wikipedia_url = data[3][0] if data[3] else None
    return wikipedia_url

@app.route('/get_weather', methods=['POST'])
def get_weather():
    api_key = "de0405115c002166202a8445e6fb9864"
    city = request.form['city']
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    
    # error message
    if response.status_code == 404:
        return render_template('index.html', error="This city does not exist. Please insert another name.")

    data = response.json()

    temperature = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    wind_speed = data["wind"]["speed"]
    weather_condition = data["weather"][0]["main"]

    # Geocoding
    location = geolocator.geocode(city)
    latitude = location.latitude
    longitude = location.longitude

    clothing = get_clothing_recommendations(temperature, weather_condition)
    activities = get_activity_recommendations(temperature, weather_condition)

    #Wikipedia URL
    wikipedia_url = get_wikipedia_url(city)

    # 3 days forecast
    forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
    forecast_response = requests.get(forecast_url)
    forecast_data = forecast_response.json()

    daily_forecasts = {}

    for entry in forecast_data['list']:
        date = entry['dt_txt'].split(' ')[0]

        if len(daily_forecasts) >= 3:
            break

        if date not in daily_forecasts:
            daily_forecasts[date] = {
                'temperature_sum': 0,
                'temperature_count': 0,
                'weather_conditions': []
            }

        daily_forecasts[date]['temperature_sum'] += entry['main']['temp']
        daily_forecasts[date]['temperature_count'] += 1
        daily_forecasts[date]['weather_conditions'].append(entry['weather'][0]['main'])

    for date, data in daily_forecasts.items():
        avg_temp = data['temperature_sum'] / data['temperature_count']
        prevalent_condition = max(set(data['weather_conditions']), key=data['weather_conditions'].count)
        
        daily_forecasts[date] = {
            'average_temperature': avg_temp,
            'condition': prevalent_condition
        }

    # put in the forecast data
    return render_template('index.html', temperature=temperature, humidity=humidity, wind_speed=wind_speed,
                           weather_condition=weather_condition, clothing=clothing, activities=activities,
                           wikipedia_url=wikipedia_url, latitude=latitude, longitude=longitude, daily_forecasts=daily_forecasts)



@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)



def get_clothing_recommendations(temperature, weather_condition):
    clothing = []
    
    if temperature < -10:
        clothing.extend(["Super heavy winter jacket", "Thermal layers", "Ice skates", "Winter hat", "Gloves", "Thermal Leggings"])
    elif temperature < 0:
        clothing.extend(["Winter coat", "Warm hoodie", "Winter boots", "Hat", "Gloves", "Ear Muffs"])
    elif temperature < 10:
        clothing.extend(["Jacket", "Sweater", "Long-sleeve shirt", "Jeans", "Long socks", "Scarf"])
    elif temperature < 20:
        clothing.extend(["Light jacket", "T-shirt", "Jeans", "Sneakers", "Windbreaker"])
    else:
        clothing.extend(["T-shirt", "Shorts", "Sandals", "Sweat-wicking Shirt", "Breathable Underwear"])

    if weather_condition == "Clear" and temperature >= 20:
        clothing.extend(["Sunglasses", "Sunscreen", "UV Protection Hat"])
    elif weather_condition in ["Rain", "Drizzle"]:
        clothing.extend(["Raincoat", "Umbrella", "Waterproof Boots", "Waterproof Pants"])
    elif weather_condition == "Snow":
        clothing.append("Gaiters")
    elif weather_condition in ["Mist", "Fog"]:
        clothing.append("Reflective Jacket")
    elif weather_condition in ["Smoke", "Haze", "Dust", "Sand", "Ash"]:
        clothing.extend(["Face Mask", "Goggles", "Long-sleeve Shirt"])
    elif weather_condition == "Thunderstorm":
        clothing.extend(["Rubber Boots", "Waterproof Jacket"])
    
    return clothing


def get_activity_recommendations(temperature, weather_condition):
    activities = []
    
    if weather_condition == "Clear":
        if temperature >= 25:
            activities.extend(["Beach Volleyball", "Surfing", "Sailing", "Kite Flying", "Paragliding"])
        elif 15 <= temperature < 25:
            activities.extend(["Tennis", "Skateboarding", "Badminton", "Mountain Climbing"])
        elif 10 <= temperature < 15:
            activities.extend(["Mountain Biking", "Trail Running", "Fishing", "Hiking", "Archery", "Rock Climbing"])
    elif weather_condition in ["Rain", "Drizzle"]:
        activities.extend(["Indoor Basketball", "Indoor Climbing", "Table Tennis", "Bowling"])
    elif weather_condition == "Snow":
        if temperature < 0:
            activities.extend(["Snowboarding", "Ice Sculpting"])
        if temperature < -5:
            activities.extend(["Skiing", "Ice Fishing"])
    elif weather_condition in ["Mist", "Fog"]:
        activities.extend(["Photography", "Indoor Yoga"])
    elif weather_condition in ["Smoke", "Haze", "Dust", "Sand", "Ash"]:
        activities.extend(["Indoor Aerobics", "Gym Workout"])
    elif weather_condition == "Thunderstorm":
        activities.extend(["Indoor Swimming", "Reading"])
    elif weather_condition == "Clouds":
        activities.extend(["Jogging", "Cycling", "Street Photography"])
    
    if not activities:
        activities.append("Yoga") 

    return activities
