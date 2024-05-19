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

2.

# Dockerfile
# Etap 1: Budowanie aplikacji
FROM python:3.9-alpine AS build

# Informacje o autorze
LABEL author="Anastasiia Pryimachuk"

# Ustawienie katalogu roboczego
WORKDIR /app

# Skopiowanie pliku requirements.txt do katalogu roboczego
COPY requirements.txt .

# Instalacja zależności
RUN pip install --no-cache-dir -r requirements.txt

# Skopiowanie reszty kodu aplikacji do katalogu roboczego
COPY . .

# Etap 2: Tworzenie finalnego obrazu
FROM python:3.9-alpine

# Informacje o autorze
LABEL author="Anastasiia Pryimachuk"

# Ustawienie katalogu roboczego
WORKDIR /app

# Kopiowanie zależności z etapu budowania
COPY --from=build /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages

# Kopiowanie całej aplikacji z etapu budowania
COPY --from=build /app /app

# Ustawienie zmiennych środowiskowych
ENV FLASK_APP=app/server.py

# Otworzenie portu, na którym serwer będzie nasłuchiwał
EXPOSE 5000

# Dodanie healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s CMD curl -f http://localhost:5000/ || exit 1

# Uruchomienie serwera Flask
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]


Komentarze:
Etap 1: Budowanie aplikacji
1."FROM python:3.9-alpine AS build":
Używam obrazu "python:3.9-alpine" jako bazowego dla etapu budowania. Alpine Linux jest bardzo lekką dystrybucją, co pomaga zmniejszyć rozmiar obrazu.
2."RUN pip install --no-cache-dir -r requirements.txt":
Instaluję zależności z pliku requirements.txt, używając flagi "--no-cache-dir", aby zminimalizować rozmiar obrazu.

Etap 2: Tworzenie finalnego obrazu
1."FROM python:3.9-alpine":
Używam obrazu python:3.9-alpine jako bazowego dla finalnego obrazu, co dalej zmniejsza jego rozmiar.
2."COPY --from=build /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages":
Kopiuję zależności Python z etapu budowania do finalnego obrazu, co pomaga zmniejszyć jego rozmiar.
3."CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]":
Ustawiam komendę uruchamiającą serwer Flask, który nasłuchuje na wszystkich interfejsach (0.0.0.0) na porcie 5000.

------------------------------------------------------------------------------------------------------------------

3.


Budowanie obrazu kontenera:
PS C:\Users\anastasiia\z1_spr\app> docker build -f Dockerfile -t docker.io/nastap/z1:z1-flask-app --push .
[+] Building 18.7s (15/15) FINISHED                                                             docker:default
 => [internal] load build definition from Dockerfile                                                      0.0s
 => => transferring dockerfile: 1.22kB                                                                    0.0s
 => [internal] load metadata for docker.io/library/python:3.9-alpine                                      1.5s
 => [auth] library/python:pull token for registry-1.docker.io                                             0.0s
 => [internal] load .dockerignore                                                                         0.0s
 => => transferring context: 2B                                                                           0.0s
 => [build 1/5] FROM docker.io/library/python:3.9-alpine@sha256:99161d2323b4130fed2d849dc8ba35274d1e1f35  0.0s
 => [internal] load build context                                                                         0.1s
 => => transferring context: 157.78kB                                                                     0.1s
 => CACHED [stage-1 2/4] WORKDIR /app                                                                     0.0s
 => CACHED [build 2/5] WORKDIR /app/app                                                                   0.0s
 => CACHED [build 3/5] COPY app/requirements.txt .                                                        0.0s
 => CACHED [build 4/5] RUN pip install --no-cache-dir -r requirements.txt                                 0.0s
 => CACHED [build 5/5] COPY ../ .                                                                         0.0s
 => CACHED [stage-1 3/4] COPY --from=build /usr/local/lib/python3.9/site-packages /usr/local/lib/python3  0.0s
 => CACHED [stage-1 4/4] COPY --from=build /app .                                                         0.0s
 => exporting to image                                                                                    0.0s
 => => exporting layers                                                                                   0.0s
 => => writing image sha256:6e2459838fdc13bbf966a48dbdb387a606aa30b1798233c7edb2022c9cbbab87              0.0s
 => => naming to docker.io/nastap/z1:z1-flask-app                                                         0.0s
 => pushing docker.io/nastap/z1:z1-flask-app with docker                                                 14.4s
 => => pushing layer dc23e643a186                                                                         8.7s
 => => pushing layer e6c040052198                                                                         9.0s
 => => pushing layer 4c2437dbcbe9                                                                         5.6s
 => => pushing layer 4857056bad11                                                                        13.8s
 => => pushing layer 69141b6c4721                                                                        13.8s
 => => pushing layer 0bbac9765c1f                                                                        13.8s
 => => pushing layer 4c9c2b9681ab                                                                        13.8s
 => => pushing layer d4fc045c9e3a                                                                        13.8s

View build details: docker-desktop://dashboard/build/default/default/i12bao5v2n3n9lhv7wqn8xt0n

Uruchomienie kontenera na podstawie zbudowanego obrazu:
PS C:\Users\anastasiia\z1_spr\app> docker run -d -p 5000:5000 --name z1-flask-container docker.io/nastap/z1:z1-flask-app
3e1cb5d17ad4188aa547d551c9198b90fe837fdf4badc53b9a15dce3301ee4c6


Sprawdzenie, ile warstw posiada zbudowany obraz:
PS C:\Users\anastasiia\z1_spr\app> docker history nastap/z1:z1-flask-app
IMAGE          CREATED             CREATED BY                                      SIZE      COMMENT
6e2459838fdc   9 minutes ago       CMD ["flask" "run" "--host=0.0.0.0" "--port=…   0B        buildkit.dockerfile.v0
<missing>      9 minutes ago       HEALTHCHECK &{["CMD-SHELL" "curl -f http://l…   0B        buildkit.dockerfile.v0
<missing>      9 minutes ago       EXPOSE map[5000/tcp:{}]                         0B        buildkit.dockerfile.v0
<missing>      9 minutes ago       ENV FLASK_APP=server.py                         0B        buildkit.dockerfile.v0
<missing>      9 minutes ago       COPY /app . # buildkit                          24.7MB    buildkit.dockerfile.v0
<missing>      About an hour ago   COPY /usr/local/lib/python3.9/site-packages …   19MB      buildkit.dockerfile.v0
<missing>      2 hours ago         WORKDIR /app                                    0B        buildkit.dockerfile.v0
<missing>      2 hours ago         LABEL author=Anastasiia Pryimachuk              0B        buildkit.dockerfile.v0
<missing>      8 weeks ago         CMD ["python3"]                                 0B        buildkit.dockerfile.v0
<missing>      8 weeks ago         RUN /bin/sh -c set -eux;   wget -O get-pip.p…   9.91MB    buildkit.dockerfile.v0
<missing>      8 weeks ago         ENV PYTHON_GET_PIP_SHA256=dfe9fd5c28dc98b5ac…   0B        buildkit.dockerfile.v0
<missing>      8 weeks ago         ENV PYTHON_GET_PIP_URL=https://github.com/py…   0B        buildkit.dockerfile.v0
<missing>      8 weeks ago         ENV PYTHON_SETUPTOOLS_VERSION=58.1.0            0B        buildkit.dockerfile.v0
<missing>      8 weeks ago         ENV PYTHON_PIP_VERSION=23.0.1                   0B        buildkit.dockerfile.v0
<missing>      8 weeks ago         RUN /bin/sh -c set -eux;  for src in idle3 p…   32B       buildkit.dockerfile.v0
<missing>      8 weeks ago         RUN /bin/sh -c set -eux;   apk add --no-cach…   29.3MB    buildkit.dockerfile.v0
<missing>      8 weeks ago         ENV PYTHON_VERSION=3.9.19                       0B        buildkit.dockerfile.v0
<missing>      8 weeks ago         ENV GPG_KEY=E3FF2839C048B25C084DEBE9B26995E3…   0B        buildkit.dockerfile.v0
<missing>      8 weeks ago         RUN /bin/sh -c set -eux;  apk add --no-cache…   1.64MB    buildkit.dockerfile.v0
<missing>      8 weeks ago         ENV LANG=C.UTF-8                                0B        buildkit.dockerfile.v0
<missing>      8 weeks ago         ENV PATH=/usr/local/bin:/usr/local/sbin:/usr…   0B        buildkit.dockerfile.v0
<missing>      3 months ago        /bin/sh -c #(nop)  CMD ["/bin/sh"]              0B
<missing>      3 months ago        /bin/sh -c #(nop) ADD file:37a76ec18f9887751…   7.38MB

Analiza obrazu:

PS C:\Users\anastasiia\z1_spr\app> docker scout cves nastap/z1:z1-flask-app
    i New version 1.8.0 available (installed version is 1.5.0) at https://github.com/docker/scout-cli
    v SBOM of image already cached, 79 packages indexed
    x Detected 7 vulnerable packages with a total of 7 vulnerabilities


## Overview

                    │           Analyzed Image
────────────────────┼─────────────────────────────────────
  Target            │  nastap/z1:z1-flask-app
    digest          │  6e2459838fdc
    platform        │ linux/amd64
    vulnerabilities │    0C     4H     4M     0L     1?
    size            │ 37 MB
    packages        │ 79