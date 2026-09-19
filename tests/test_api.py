from fastapi.testclient import TestClient

from support_gateway import api


client = TestClient(api.app)

AUTH_HEADERS = {
    "Authorization": f"Bearer {api.APP_API_KEY}",
}