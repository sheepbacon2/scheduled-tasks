import os
from twilio.rest import Client
from datetime import datetime
import requests


account_sid = os.environ.get("ACCOUNT_SID")
auth_token = os.environ.get("AUTH_TOKEN")
client = Client(account_sid, auth_token)
url = "https://api.openweathermap.org/data/2.5/forecast"
api_key = os.environ.get("OWM_API_KEY")
params = {
    "appid": api_key,
    "lat": 37.283127,
    "lon": -121.991430,
    "units": "imperial",
    "cnt": 4,
}

response = requests.get(url, params=params)
print (response.url)
response.raise_for_status()
weather_data = response.json()
rain_time = []
will_rain = False
for weather in weather_data["list"]:
    condition_code = weather["weather"][0]["id"]
    if int(condition_code) < 700:
        will_rain = True
        rain_time.append(weather["dt_txt"])

try:
    rain_time_date = rain_time[0][5:10] #splits off year
    rain_time_nearest = rain_time[0].split()[-1]
    dt_object = datetime.strptime(rain_time_nearest, "%H:%M:%S")
    rain_time2 = dt_object.strftime("%I:%M %p")
except IndexError:
    print("No rain time found")



if will_rain:
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        from_="whatsapp:+14155238886",
        body=f"It's going to rain on {rain_time_date} "
             f"at {rain_time2}",
        to=f"whatsapp:{os.environ.get("WHATSAPP"}"
    )
    print(message.status)
