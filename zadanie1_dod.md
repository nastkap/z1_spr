1.
#server.py
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
    logging.info(f"Nasłuch na porcie TCP: {TCP_PORT}")

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


Uwagi:
1. Serwer loguje czas uruchomienia, imię i nazwisko autora oraz port do pliku logów server.log.
2. Serwer pobiera strefę czasową klienta na podstawie jego adresu IP, korzystając z API ipinfo.io.
3. Serwer Flask dynamicznie renderuje stronę HTML wyświetlającą adres IP klienta oraz aktualny czas w jego strefie czasowej.

-----------------------------------------------------------------------------------------

4.

# Dockerfile

# syntax=docker/dockerfile:1.2-stable

# Etap 1: Budowanie aplikacji
FROM python:3.9-alpine AS build

# Informacje o autorze
LABEL author="Anastasiia Pryimachuk"

# Ustawienie katalogu roboczego
WORKDIR /app/app

# Skopiowanie pliku requirements.txt do katalogu roboczego
COPY app/requirements.txt .

# Instalacja zależności
RUN --mount=type=cache,target=/root/.cache/pip pip install --no-cache-dir -r requirements.txt

# Skopiowanie reszty kodu aplikacji do katalogu roboczego
COPY ../ .

# Etap 2: Tworzenie finalnego obrazu
FROM python:3.9-alpine

# Informacje o autorze
LABEL author="Anastasiia Pryimachuk"

# Ustawienie katalogu roboczego
WORKDIR /app

# Kopiowanie zależności z etapu budowania
COPY --from=build /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages

# Kopiowanie całej aplikacji z etapu budowania
COPY --from=build /app .

# Ustawienie zmiennych środowiskowych
ENV FLASK_APP=server.py

# Otworzenie portu, na którym serwer będzie nasłuchiwał
EXPOSE 5000

# Dodanie healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s CMD curl -f http://localhost:5000/ || exit 1

# Uruchomienie serwera Flask
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]


-------------------------------------------------------------------------------------
Budowanie obrazu:
PS C:\Users\anastasiia\z1_spr\app> docker buildx build -f Dockerfile_dod -t docker.io/nastap/z1:czn-z4-dod --platform linux/amd64,linux/arm64 --push .
[+] Building 75.2s (23/23) FINISHED                                                        docker-container:z1builder
 => [internal] load build definition from Dockerfile_dod                                                         0.0s
 => => transferring dockerfile: 1.31kB                                                                           0.0s
 => [linux/amd64 internal] load metadata for docker.io/library/python:3.9-alpine                                 1.0s
 => [linux/arm64 internal] load metadata for docker.io/library/python:3.9-alpine                                 1.0s
 => [internal] load .dockerignore                                                                                0.0s
 => => transferring context: 2B                                                                                  0.0s
 => [internal] load build context                                                                                0.3s
 => => transferring context: 157.82kB                                                                            0.2s
 => [linux/amd64 build 1/5] FROM docker.io/library/python:3.9-alpine@sha256:99161d2323b4130fed2d849dc8ba35274d1  0.0s
 => => resolve docker.io/library/python:3.9-alpine@sha256:99161d2323b4130fed2d849dc8ba35274d1e1f35da170435627b2  0.0s
 => [linux/arm64 build 1/5] FROM docker.io/library/python:3.9-alpine@sha256:99161d2323b4130fed2d849dc8ba35274d1  0.0s
 => => resolve docker.io/library/python:3.9-alpine@sha256:99161d2323b4130fed2d849dc8ba35274d1e1f35da170435627b2  0.0s
 => CACHED [linux/arm64 stage-1 2/4] WORKDIR /app                                                                0.0s
 => CACHED [linux/amd64 stage-1 2/4] WORKDIR /app                                                                0.0s
 => CACHED [linux/amd64 build 2/5] WORKDIR /app/app                                                              0.0s
 => CACHED [linux/amd64 build 3/5] COPY app/requirements.txt .                                                   0.0s
 => CACHED [linux/amd64 build 4/5] RUN --mount=type=cache,target=/root/.cache/pip pip install --no-cache-dir -r  0.0s
 => CACHED [linux/amd64 build 5/5] COPY ../ .                                                                    0.0s
 => CACHED [linux/amd64 stage-1 3/4] COPY --from=build /usr/local/lib/python3.9/site-packages /usr/local/lib/py  0.0s
 => CACHED [linux/amd64 stage-1 4/4] COPY --from=build /app .                                                    0.0s
 => CACHED [linux/arm64 build 2/5] WORKDIR /app/app                                                              0.0s
 => CACHED [linux/arm64 build 3/5] COPY app/requirements.txt .                                                   0.0s
 => [linux/arm64 build 4/5] RUN --mount=type=cache,target=/root/.cache/pip pip install --no-cache-dir -r requi  51.0s
 => [linux/arm64 build 5/5] COPY ../ .                                                                           0.4s
 => [linux/arm64 stage-1 3/4] COPY --from=build /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9  0.4s
 => [linux/arm64 stage-1 4/4] COPY --from=build /app .                                                           0.4s
 => exporting to image                                                                                          21.0s
 => => exporting layers                                                                                          1.5s
 => => exporting manifest sha256:70ab1356b2aae3c5f7720e9b22daa836beca37ef75a7c70948dc289c13512e78                0.0s
 => => exporting config sha256:716b7fef013b4da02a1bec74599f9a1e7109c47b2384818c079b432fe9411d8f                  0.0s
 => => exporting attestation manifest sha256:d2173294412b299a4e4e5475c988f81415baae0c2cdad2ff2acd8294029d63bb    0.0s
 => => exporting manifest sha256:199cfd2440015d91f22f5feec6685014184467da08d75baae4cf1ae48808a41e                0.0s
 => => exporting config sha256:bceca381b5db30d4749151506af8375e7a7733250c8566bd44e934c81f4dd6f8                  0.0s
 => => exporting attestation manifest sha256:65113e762c1b7d1b798c278b9c4a3afb4283a115347bcb6098383084c65370b4    0.0s
 => => exporting manifest list sha256:0cddc166394bbdd14a710cef7043188dc28edca591090e31dc3c2658df3d7332           0.0s
 => => pushing layers                                                                                           17.0s
 => => pushing manifest for docker.io/nastap/z1:czn-z4-dod@sha256:0cddc166394bbdd14a710cef7043188dc28edca591090  2.3s
 => [auth] nastap/z1:pull,push token for registry-1.docker.io                                                    0.0s

View build details: docker-desktop://dashboard/build/z1builder/z1builder0/uht9kmicc2b8ov1742rg2o4nf
PS C:\Users\anastasiia\z1_spr\app>