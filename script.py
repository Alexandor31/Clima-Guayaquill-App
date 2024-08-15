import requests
import os
import csv
from datetime import datetime

# Datos de la API
GUAYAQUIL_LAT = -2.170998
GUAYAQUIL_LONGITUDE = -79.922359
API_KEY = "960b0c601a2c3df27159443a7d1eca75"
FILE_NAME = "/home/alexander/ArquitecturaComputadores/ProyectoII/clima-guayaquil-hoy.csv"
LOG_FILE = "/home/alexander/ArquitecturaComputadores/ProyectoII/registro.log"

def log_message(message):
    with open(LOG_FILE, 'a') as log_file:
        log_file.write(f"{datetime.now()}: {message}\n")

def get_weather(lat, lon, api):
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api}&units=metric"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Lanza una excepción para códigos de estado HTTP erróneos
        return response.json()
    except requests.RequestException as e:
        log_message(f"Error fetching weather data: {e}")
        return None

def write2csv(json_response, csv_filename):
    if json_response is None:
        return

    # Verifica si el archivo existe para escribir los encabezados solo una vez
    file_exists = os.path.isfile(csv_filename)
    
    try:
        with open(csv_filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            if not file_exists:
                # Escribe todos los encabezados en el CSV
                writer.writerow([
                    'dt', 'coord_lon', 'coord_lat', 'weather_0_id', 'weather_0_main', 'weather_0_description', 
                    'weather_0_icon', 'base', 'main_temp', 'main_feels_like', 'main_temp_min', 'main_temp_max', 
                    'main_pressure', 'main_humidity', 'main_sea_level', 'main_grnd_level', 'visibility', 'wind_speed', 
                    'wind_deg', 'wind_gust', 'clouds_all', 'sys_type', 'sys_id', 'sys_country', 'sys_sunrise', 
                    'sys_sunset', 'timezone', 'id', 'name', 'cod'
                ])
            
            # Escribe todos los valores en una fila del CSV
            writer.writerow([
                json_response.get('dt', ''),
                json_response.get('coord', {}).get('lon', ''),
                json_response.get('coord', {}).get('lat', ''),
                json_response.get('weather', [{}])[0].get('id', ''),
                json_response.get('weather', [{}])[0].get('main', ''),
                json_response.get('weather', [{}])[0].get('description', ''),
                json_response.get('weather', [{}])[0].get('icon', ''),
                json_response.get('base', ''),
                json_response.get('main', {}).get('temp', ''),
                json_response.get('main', {}).get('feels_like', ''),
                json_response.get('main', {}).get('temp_min', ''),
                json_response.get('main', {}).get('temp_max', ''),
                json_response.get('main', {}).get('pressure', ''),
                json_response.get('main', {}).get('humidity', ''),
                json_response.get('main', {}).get('sea_level', ''),
                json_response.get('main', {}).get('grnd_level', ''),
                json_response.get('visibility', ''),
                json_response.get('wind', {}).get('speed', ''),
                json_response.get('wind', {}).get('deg', ''),
                json_response.get('wind', {}).get('gust', ''),
                json_response.get('clouds', {}).get('all', ''),
                json_response.get('sys', {}).get('type', ''),
                json_response.get('sys', {}).get('id', ''),
                json_response.get('sys', {}).get('country', ''),
                json_response.get('sys', {}).get('sunrise', ''),
                json_response.get('sys', {}).get('sunset', ''),
                json_response.get('timezone', ''),
                json_response.get('id', ''),
                json_response.get('name', ''),
                json_response.get('cod', '')
            ])
        
        log_message("Datos guardados correctamente")
    except Exception as e:
        log_message(f"Error writing to CSV: {e}")

def main():
    print("===== Bienvenido a Guayaquil-Clima =====")
    guayaquil_weather = get_weather(lat=GUAYAQUIL_LAT, lon=GUAYAQUIL_LONGITUDE, api=API_KEY)
    if guayaquil_weather and guayaquil_weather.get('cod') != 404:
        write2csv(guayaquil_weather, FILE_NAME)
    else:
        log_message("Ciudad no disponible o API KEY no válida")

if __name__ == '__main__':
    main()
