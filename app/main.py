
from fastapi import FastAPI

app = FastAPI(
    title="CitizenTech - CivicLens API",
    description="API simplificada de gerenciamento de ocorrências urbanas",
    version="1.0.0"
)

ocorrencias = [
    {
        "id": 1,
        "tipo": "Iluminacao publica",
        "bairro": "Centro",
        "status": "aberta"
    },
    {
        "id": 2,
        "tipo": "Buraco na via",
        "bairro": "Jardim Paulista",
        "status": "em andamento"
    }
]


@app.get("/health")
def verificar_saude():
    return {"status": "ok"}


@app.get("/ocorrencias")
def listar_ocorrencias():
    return {
        "total": len(ocorrencias),
        "dados": ocorrencias
    }
