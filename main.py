from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

# Inizializza l'app FastAPI
app = FastAPI(
    title="FastAPI Demo su Coolify",
    description="Applicazione di esempio per deployment su Coolify",
    version="1.0.0"
)

# Configura CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelli Pydantic
class Item(BaseModel):
    id: Optional[int] = None
    name: str
    description: Optional[str] = None
    price: float

class Message(BaseModel):
    message: str
    status: str

# Database in memoria (per demo)
items_db: List[Item] = [
    Item(id=1, name="Laptop", description="Computer portatile", price=999.99),
    Item(id=2, name="Mouse", description="Mouse wireless", price=29.99),
]

# Routes
@app.get("/", response_model=Message)
async def root():
    """Endpoint principale"""
    return {
        "message": "Benvenuto nell'API FastAPI su Coolify!",
        "status": "success"
    }

@app.get("/health")
async def health_check():
    """Health check per Coolify"""
    return {
        "status": "healthy",
        "service": "fastapi-demo"
    }

@app.get("/items", response_model=List[Item])
async def get_items():
    """Ottieni tutti gli items"""
    return items_db

@app.get("/items/{item_id}", response_model=Item)
async def get_item(item_id: int):
    """Ottieni un item specifico"""
    for item in items_db:
        if item.id == item_id:
            return item
    return {"message": "Item non trovato", "status": "error"}

@app.post("/items", response_model=Item)
async def create_item(item: Item):
    """Crea un nuovo item"""
    # Genera ID automaticamente
    if not item.id:
        item.id = max([i.id for i in items_db], default=0) + 1
    items_db.append(item)
    return item

@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, item: Item):
    """Aggiorna un item esistente"""
    for i, existing_item in enumerate(items_db):
        if existing_item.id == item_id:
            item.id = item_id
            items_db[i] = item
            return item
    return {"message": "Item non trovato", "status": "error"}

@app.delete("/items/{item_id}", response_model=Message)
async def delete_item(item_id: int):
    """Elimina un item"""
    for i, item in enumerate(items_db):
        if item.id == item_id:
            items_db.pop(i)
            return {
                "message": f"Item {item_id} eliminato con successo",
                "status": "success"
            }
    return {"message": "Item non trovato", "status": "error"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)