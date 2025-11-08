# FastAPI Demo per Coolify

Applicazione FastAPI di esempio pronta per il deployment su Coolify.

## 🚀 Caratteristiche

- API RESTful completa con operazioni CRUD
- Health check endpoint per Coolify
- Documentazione automatica (Swagger UI e ReDoc)
- Gestione CORS
- Docker-ready

## 📦 Struttura del Progetto

```
fastapi-coolify/
├── main.py              # Applicazione principale
├── requirements.txt     # Dipendenze Python
├── Dockerfile          # Configurazione Docker
├── .dockerignore       # File da escludere dal build
└── README.md           # Questa documentazione
```

## 🔧 Installazione Locale

### Prerequisiti
- Python 3.11+
- pip

### Setup

1. Clona il repository
```bash
git clone <your-repo-url>
cd fastapi-coolify
```

2. Crea un ambiente virtuale
```bash
python -m venv venv
source venv/bin/activate  # Su Windows: venv\Scripts\activate
```

3. Installa le dipendenze
```bash
pip install -r requirements.txt
```

4. Avvia l'applicazione
```bash
uvicorn main:app --reload
```

L'API sarà disponibile su `http://localhost:8000`

## 📚 Documentazione API

Una volta avviata l'applicazione, puoi accedere a:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 🔌 Endpoints Disponibili

### GET /
Endpoint principale che restituisce un messaggio di benvenuto

### GET /health
Health check per monitoraggio (usato da Coolify)

### GET /items
Ottieni la lista di tutti gli items

### GET /items/{item_id}
Ottieni un item specifico per ID

### POST /items
Crea un nuovo item

**Body:**
```json
{
  "name": "string",
  "description": "string",
  "price": 0
}
```

### PUT /items/{item_id}
Aggiorna un item esistente

### DELETE /items/{item_id}
Elimina un item

## 🐳 Docker

### Build dell'immagine
```bash
docker build -t fastapi-demo .
```

### Run del container
```bash
docker run -p 8000:8000 fastapi-demo
```

## ☁️ Deploy su Coolify

### Configurazione Coolify

1. **Port Exposes**: `8000`
2. **Health Check Path**: `/health`
3. **Build Pack**: Dockerfile
4. **Environment Variables**: Nessuna richiesta per questa demo

### Deploy Automatico

Coolify effettuerà automaticamente il deploy ad ogni push sul branch configurato.

## 🧪 Test

Puoi testare l'API usando curl:

```bash
# Health check
curl http://your-domain.com/health

# Get items
curl http://your-domain.com/items

# Create item
curl -X POST http://your-domain.com/items \
  -H "Content-Type: application/json" \
  -d '{"name":"Tastiera","description":"Meccanica RGB","price":89.99}'
```

## 📝 Note

- Questa è un'applicazione di demo che usa un database in memoria
- Per produzione, considera l'integrazione con un database reale (PostgreSQL, MongoDB, etc.)
- Aggiungi autenticazione/autorizzazione per endpoint sensibili
- Configura variabili d'ambiente per configurazioni specifiche

## 📄 Licenza

MIT License