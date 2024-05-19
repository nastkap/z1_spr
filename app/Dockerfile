# Etap 1: Budowanie aplikacji
FROM python:3.9-alpine AS build

# Informacje o autorze
LABEL author="Anastasiia Pryimachuk"

# Ustawienie katalogu roboczego
WORKDIR /app/app

# Skopiowanie pliku requirements.txt do katalogu roboczego
COPY app/requirements.txt .

# Instalacja zależności
RUN pip install --no-cache-dir -r requirements.txt

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
