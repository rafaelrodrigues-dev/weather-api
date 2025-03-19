import os
from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

def get_current_weather(city):
    API_KEY = os.environ.get('API_KEY','')

    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=pt'
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erro na requisição: {response.text}")
        return None

@app.route('/api/v1/weather', methods=['GET'])
def weather():
    city = request.args.get('city')
    if not city:
        return jsonify({"error": "Parâmetro 'city' é obrigatório"}), 400

    weather_data = get_current_weather(city)
    if weather_data:
        return jsonify(weather_data)
    else:
        return jsonify({"error": "Unable to obtain weather data"}), 404

if __name__ == '__main__':
    app.run()