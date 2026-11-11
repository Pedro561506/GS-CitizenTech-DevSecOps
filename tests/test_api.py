
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_ocorrencias():
    response = client.get("/ocorrencias")

    assert response.status_code == 200
    assert response.json()["total"] == 2
    assert len(response.json()["dados"]) == 2

    def test_falha_controlada():
    """Teste temporario para demonstrar o bloqueio da pipeline."""
    assert 1 == 2
