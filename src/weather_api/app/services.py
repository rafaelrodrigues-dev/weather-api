import requests

def convert_time(time_str: str):
    """
    Convert time string from HHMM format to HH:MM format.
    :param time_str: Time string in HHMM format
    :return: Time string in HH:MM format
    """
    time_padded = time_str.zfill(4)
    return f'{time_padded[:2]}:{time_padded[2:]}'

def get_current_weather(city: str, lang: str):
    url = f'https://wttr.in/{city}/'
    response = requests.get(url, params={'format':'j1', 'lang':lang}, timeout=5)

    if response.status_code == 200:
        current_condition = response.json()['current_condition'][0]
        city = response.json()['nearest_area'][0]['areaName'][0]['value']
        if hasattr(current_condition, 'lang_xx'):
            description = current_condition['lang_xx'][0]['value']
        else:
            description = current_condition['weatherDesc'][0]['value']
        return {
            'areaName': city,
            'observation_time': current_condition['observation_time'],
            'temp_C': current_condition['temp_C'],
            'FeelsLikeC': current_condition['FeelsLikeC'],
            'weatherDesc': description,
            'humidity': current_condition['humidity'],
            'precipMM': current_condition['precipMM'],
            'uvIndex': current_condition['uvIndex'],
            'windspeedKmph': current_condition['windspeedKmph'],
            'winddir16Point': current_condition['winddir16Point'],
            'weatherIconUrl': current_condition['weatherIconUrl'][0]['value'],
        }

    else:
        return None

def get_forecast_weather(city: str, lang: str):
    url = f'https://wttr.in/{city}/'
    response = requests.get(url, params={'format':'j1', 'lang':lang},timeout=5)

    if response.status_code == 200:
        weather = response.json()['weather']
        city = response.json()['nearest_area'][0]['areaName'][0]['value']
        forecasts = []

        for day in weather:
            forecast = {
                'areaName': city,
                'date': day['date'],
                'avgtempC': day['avgtempC'],
                'mintempC': day['mintempC'],
                'maxtempC': day['maxtempC'],
                'uvIndex': day['uvIndex'],
                'sunrise': day['astronomy'][0]['sunrise'],
                'sunset': day['astronomy'][0]['sunset'],
                'hourly': []
            }
            
            for i in range(0, len(day['hourly']), 2):
                time = day['hourly'][i]
                if hasattr(time, 'lang_xx'):
                    description = time['lang_xx'][0]['value']
                else:
                    description = time['weatherDesc'][0]['value']
                forecast['hourly'].append(
                    {
                        'time': convert_time(time['time']),
                        'tempC': time['tempC'],
                        'FeelsLikeC': time['FeelsLikeC'],
                        'weatherDesc': description,
                        'humidity': time['humidity'],
                        'precipMM': time['precipMM'],
                        'chanceofrain': time['chanceofrain'],
                        'windspeedKmph': time['windspeedKmph'],
                        'windspeedMiles': time['windspeedMiles'],
                        'weatherIconUrl': time['weatherIconUrl'][0]['value'],
                    }
                )
            forecasts.append(forecast)
        return forecasts

    else:
        return None