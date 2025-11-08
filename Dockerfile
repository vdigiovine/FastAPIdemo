# Usa un'immagine Python ufficiale
FROM python:3.11-slim

# Imposta la directory di lavoro
WORKDIR /app

# Copia i file dei requisiti
COPY requirements.txt .

# Installa le dipendenze
RUN pip install --no-cache-dir -r requirements.txt

# Copia il codice dell'applicazione
COPY . .

# Esponi la porta 8000
EXPOSE 8000

# Comando per avviare l'applicazione
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]