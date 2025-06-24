from dotenv import load_dotenv
load_dotenv()

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.api import vision_routes  # <- Caminho do router

app = FastAPI(title="DilsAI Vision - API", version="1.0")

# Garante que a pasta existe
os.makedirs("data/output", exist_ok=True)

# Servindo arquivos estáticos (imagens geradas)
app.mount("/data/output", StaticFiles(directory="data/output"), name="output")

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Pode deixar aberto por enquanto
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rota principal
@app.get("/")
def read_root():
    return {"mensagem": "🚀 DilsAI Vision API no ar com sucesso!"}

# Importa as rotas da visão
app.include_router(vision_routes.router)
