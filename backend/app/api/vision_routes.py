# app/api/vision_routes.py

from fastapi import APIRouter
from pydantic import BaseModel
from uuid import uuid4
from datetime import datetime
import requests
import json
import os
from openai import OpenAI  # Cliente novo!

router = APIRouter()

# 💡 Recomendado usar variável de ambiente
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class PromptRequest(BaseModel):
    prompt: str

@router.post("/gerar-imagem")
async def gerar_imagem(req: PromptRequest):
    response = client.images.generate(
        model="dall-e-3",
        prompt=req.prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )

    url_img = response.data[0].url
    nome_arquivo = f"{uuid4().hex}.png"
    caminho_arquivo = f"data/output/{nome_arquivo}"

    # Baixa e salva a imagem
    img_data = requests.get(url_img).content
    with open(caminho_arquivo, "wb") as f:
        f.write(img_data)

    # Histórico
    historico_path = "data/output/historico.json"
    entrada = {
        "prompt": req.prompt,
        "arquivo": nome_arquivo,
        "data": datetime.now().isoformat(),
        "url_local": f"/data/output/{nome_arquivo}"
    }

    if os.path.exists(historico_path):
        with open(historico_path, "r", encoding="utf-8") as f:
            historico = json.load(f)
    else:
        historico = []

    historico.append(entrada)

    with open(historico_path, "w", encoding="utf-8") as f:
        json.dump(historico, f, indent=4, ensure_ascii=False)

    return {"imagem": f"http://127.0.0.1:8000/{entrada['url_local']}"}
