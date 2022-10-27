import requests
import json



def pobierzpogode():
  r = requests.get('http://api.openweathermap.org/data/2.5/weather?q=Warszawa&appid=14462c10b85633a0a6d5a2729ec1ded2')
  loc_weather = r.content.strip()

  temp,humid,weathertype,rain, pressure, wind = zwroc_elementy_pogody(loc_weather)
  return temp, humid, weathertype, rain, pressure, wind



def zwroc_elementy_pogody(wynik_pogody):
  json_pogody = json.loads(wynik_pogody)
  temp_k = json_pogody["main"]["temp"]
  temp_c = konwertuj_do_c(temp_k)
  humid = json_pogody["main"]["humidity"]
  pressure = json_pogody["main"]["pressure"]
  wind = json_pogody["wind"]["speed"]
  weathertype = json_pogody["weather"][0]["main"]
  rain = "Rain" if weathertype=="rain" else "no rain"
  return temp_c, humid, weathertype, rain, pressure, wind


def konwertuj_do_c(k):
  return str(round(float(k) - 273.15,2))