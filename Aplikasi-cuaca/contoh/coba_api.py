import requests

url = "https://api.open-meteo.com/v1/forecast"
parameter = {
    "latitude": -0.03,
    "longitude": 109.33,
    "current": "temperature_2m"
}

respon = requests.get(url, params=parameter)

print("Status", respon.status_code)
data = respon.json()
print(data["current"]["temperature_2m"])