from fastapi.testclient import TestClient
from ..main import app

client = TestClient(app)

# same test name convention applies here as well
def test_easteregg():
    assert client.get("easterEgg").text == '"Easter Egg, codebase changed"'
    

