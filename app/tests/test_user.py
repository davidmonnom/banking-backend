
from fastapi.testclient import TestClient

from ..main import app
from .overrides import get_logged_user_override, get_db_override
from ..security import get_logged_user, get_db

client = TestClient(app)
app.dependency_overrides[get_logged_user] = get_logged_user_override
app.dependency_overrides[get_db] = get_db_override


def test_user():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "You are very welcome, john.doe@example.com!"}
