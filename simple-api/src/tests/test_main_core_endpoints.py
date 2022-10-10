"""TEST MAIN CORE ENDPOINTS"""
from fastapi.testclient import TestClient
from simple_api import main
import pytest
from dotenv import load_dotenv

client = TestClient(main.app)


@pytest.fixture(scope='session', autouse=True)
def load_env():
    load_dotenv()


def test_main_health_endpoint():
    """Tests health endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {
        "message": "OK",
        "description": "Service is up and running",
    }


def test_main_version_endpoint():
    """Tests version endpoint"""
    response = client.get("/version")
    assert response.status_code == 200
    assert response.json() == {
        "message": "0.0.1",
    }
