import requests
import winreg
import ctypes
import traceback
import os

COLD_THRESHOLD = 12
HOT_THRESHOLD = 24
API_KEY = os.getenv("OPEN_WAETHER_API_KEY")
print(API_KEY, "Hey")
wallpaper_folder = r"C:\Users\joshu\OneDrive\Desktop\Fun Builds\Weather desktop wallpaper"
 

clouds = "clouds.jpg"
clouds_cold = "clouds_cold.jpg"
clouds_hot = "clouds_hot.jpg"

rain = "rain.jpg"
rain_cold = "rain_cold.jpg"
rain_hot = "rain_hot.jpg"

clear = "clear.jpg"
clear_cold = "clear_cold.jpg" 
clear_hot = "clear_hot.jpg"

other = "other.jpg"
other_cold = "other_cold.jpg"
other_hot = "other_hot.jpg"

def get_lat_and_lon():
    LOCATION = "Richmond, NZ"
    location_and_key = {'appid': API_KEY,
                        "q": LOCATION,
                        "limit": "1"}
    
    r_cordates = requests.get('http://api.openweathermap.org/geo/1.0/direct', params=location_and_key)
    data_cordates = r_cordates.json()

    lat = data_cordates[0]["lat"]
    lon = data_cordates[0]["lon"]
    return lat, lon

def get_temp_type(temp):
    if temp < COLD_THRESHOLD:
      return"cold"

    elif temp > HOT_THRESHOLD:
       return "hot"

    else:
       return "normal"

def get_data(lat, lon):
    parameters = {'lat':f"{lat}", 'lon':f"{lon}", 'appid': API_KEY}
    r = requests.get('https://api.openweathermap.org/data/2.5/weather', params=parameters)
    return r.json()


def get_temp_type_and_weather_type(lat, lon):
    data = get_data(lat, lon)
    temp = round(data["main"]["temp"] - 273.15, 1)

    temp_type = get_temp_type(temp)
    weather_type = data["weather"][0]["main"]
    
    
    if weather_type not in ("Clouds", "Clear", "Rain"):
        weather_type = "Other"

    return temp_type, weather_type

def get_wallpaper(temp_type, weather_type):

    weather_types = {
        "Clouds": {"cold": clouds_cold, "hot": clouds_hot, "normal": clouds},
        "Clear": {"cold": clear_cold, "hot": clear_hot, "normal": clear},
        "Rain": {"cold": rain_cold, "hot": rain_hot, "normal": rain},
        "Other": {"cold": other_cold, "hot": other_hot, "normal": other},
        }
    
    return weather_types[weather_type][temp_type]

def update_wallpaper_path(wallpaper_path):
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Control Panel\Desktop", 0, winreg.KEY_SET_VALUE) as key:
        winreg.SetValueEx(key, "Wallpaper", 0, 1, wallpaper_path)

def refresh_wallpaper(wallpaper_path):
    SPI_WALLPAPER = 20 
    ctypes.windll.user32.SystemParametersInfoW(SPI_WALLPAPER, 0, wallpaper_path, 3)



def change_and_update_wallpaper(wallpaper):
    wallpaper_path = rf"{wallpaper_folder}\{wallpaper}"
    update_wallpaper_path(wallpaper_path)
    refresh_wallpaper(wallpaper_path)
    
def main():    
    print
    try:
        lat, lon = get_lat_and_lon()
        temp_type, weather_type = get_temp_type_and_weather_type(lat, lon)

        wallpaper = get_wallpaper(temp_type, weather_type)
        change_and_update_wallpaper(wallpaper)

    except Exception:
        with open(rf"{wallpaper_folder}\error_loging.txt", "w") as f:
            f.write(traceback.format_exc())
main()


