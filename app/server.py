# /app/server.py

from flask import Flask, request, render_template_string
import logging
from datetime import datetime
import requests

# Konfiguracja
AUTHOR_NAME = "Anastasiia Pryimachuk"
TCP_PORT = 5000
LOG_FILE = 'server.log'

# Inicjalizacja aplikacji Flask
app = Flask(__name__)

# Konfiguracja logowania
logging.basicConfig(filename=LOG_FILE, level=logging.INFO)

# Funkcja logująca informacje o uruchomieniu serwera
def log_server_start():
    start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    logging.info(f"Serwer uruchomiony: {start_time}")
    logging.info(f"Autor: {AUTHOR_NAME}")
    logging.info(f"Nasluch na porcie TCP: {TCP_PORT}")

# Funkcja pobierająca informacje o strefie czasowej na podstawie IP
def get_timezone_info(ip):
    response = requests.get(f"https://ipinfo.io/{ip}/json")
    data = response.json()
    timezone = data.get('timezone', 'UTC')
    return timezone

# Trasa Flask do obsługi połączeń klienta
@app.route('/')
def index():
    client_ip = request.remote_addr
    timezone = get_timezone_info(client_ip)
    current_time = datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S')
    return render_template_string("""
        <h1>Informacje o kliencie</h1>
        <p>Adres IP: {{ client_ip }}</p>
        <p>Lokalny czas: {{ current_time }}</p>
    """, client_ip=client_ip, current_time=current_time)

if __name__ == '__main__':
    log_server_start()
    app.run(host='0.0.0.0', port=TCP_PORT)
