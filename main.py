from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.orm import Session
import uvicorn

from backend.database import get_db, init_db, ItemDB

# Inizializza l'app FastAPI
app = FastAPI(
    title="FastAPI Demo su Coolify",
    description="Applicazione di esempio per deployment su Coolify con PostgreSQL",
    version="2.0.0",
    servers=[
        {"url": "https://api.luceramultimedia.it", "description": "Production"},
        {"url": "http://localhost:8000", "description": "Development"}
    ]
)

# Middleware per trusted hosts (sicurezza)
app.add_middleware(
    TrustedHostMiddleware, 
    allowed_hosts=["api.luceramultimedia.it", "localhost", "127.0.0.1", "*"]
)

# Configura CORS per permettere richieste dal frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://frontend.luceramultimedia.it",
        "https://coolify.digiovine.info",
        "http://localhost:5173",  # Vite dev server
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware per forzare HTTPS in produzione e aggiungere header di sicurezza
@app.middleware("http")
async def security_middleware(request: Request, call_next):
    response = await call_next(request)
    
    # Aggiungi header di sicurezza
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    
    return response

# Modelli Pydantic per request/response
class ItemCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float

class ItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None

class Item(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float
    
    class Config:
        from_attributes = True

class Message(BaseModel):
    message: str
    status: str

# Event: Inizializza database all'avvio
@app.on_event("startup")
async def startup_event():
    init_db()
    print("✅ Database inizializzato")

# Routes
@app.get("/", response_model=Message)
async def root():
    """Endpoint principale"""
    return {
        "message": "Benvenuto nell'API FastAPI su Coolify con PostgreSQL!",
        "status": "success"
    }

@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    """Health check per Coolify - verifica anche la connessione al database"""
    try:
        # Testa la connessione al database
        db.execute("SELECT 1")
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"
    
    return {
        "status": "healthy",
        "service": "fastapi-demo",
        "version": "2.0.0",
        "database": db_status
    }

@app.get("/healthz")
async def kubernetes_health():
    """Alternative health check endpoint (Kubernetes style)"""
    return {"status": "ok"}

@app.get("/ready")
async def readiness_check(db: Session = Depends(get_db)):
    """Readiness check - verifica che l'app sia pronta a ricevere traffico"""
    try:
        db.execute("SELECT 1")
        db_ready = True
    except:
        db_ready = False
    
    return {
        "status": "ready" if db_ready else "not_ready",
        "checks": {
            "api": "ok",
            "database": "ok" if db_ready else "error"
        }
    }

@app.get("/items", response_model=List[Item])
async def get_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Ottieni tutti gli items dal database"""
    items = db.query(ItemDB).offset(skip).limit(limit).all()
    return items

@app.get("/items/{item_id}", response_model=Item)
async def get_item(item_id: int, db: Session = Depends(get_db)):
    """Ottieni un item specifico"""
    item = db.query(ItemDB).filter(ItemDB.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item non trovato")
    return item

@app.post("/items", response_model=Item, status_code=201)
async def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    """Crea un nuovo item"""
    db_item = ItemDB(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, item: ItemUpdate, db: Session = Depends(get_db)):
    """Aggiorna un item esistente"""
    db_item = db.query(ItemDB).filter(ItemDB.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item non trovato")
    
    # Aggiorna solo i campi forniti
    update_data = item.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_item, key, value)
    
    db.commit()
    db.refresh(db_item)
    return db_item

@app.delete("/items/{item_id}", response_model=Message)
async def delete_item(item_id: int, db: Session = Depends(get_db)):
    """Elimina un item"""
    db_item = db.query(ItemDB).filter(ItemDB.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item non trovato")
    
    db.delete(db_item)
    db.commit()
    return {
        "message": f"Item {item_id} eliminato con successo",
        "status": "success"
    }

# Endpoint per popolare il database con dati di esempio
@app.post("/seed", response_model=Message)
async def seed_database(db: Session = Depends(get_db)):
    """Popola il database con dati di esempio"""
    # Verifica se ci sono già dati
    existing_items = db.query(ItemDB).count()
    if existing_items > 0:
        return {
            "message": f"Database già popolato con {existing_items} items",
            "status": "info"
        }
    
    # Dati di esempio
    sample_items = [
        ItemDB(name="Laptop", description="Computer portatile ad alte prestazioni", price=999.99),
        ItemDB(name="Mouse", description="Mouse wireless ergonomico", price=29.99),
        ItemDB(name="Tastiera", description="Tastiera meccanica RGB", price=89.99),
        ItemDB(name="Monitor", description="Monitor 27 pollici 4K", price=399.99),
        ItemDB(name="Webcam", description="Webcam Full HD 1080p", price=79.99),
    ]
    
    db.add_all(sample_items)
    db.commit()
    
    return {
        "message": f"Database popolato con {len(sample_items)} items di esempio",
        "status": "success"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)