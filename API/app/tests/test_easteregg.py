from fastapi.testclient import TestClient
from ..main import app

client = TestClient(app)

# same test name convention applies here as well
def test_easteregg():
    assert client.get("easterEgg").text == '"Easter Egg, codebase changed"'
    
def test_create_user():
    # don't forget the last / in the endpoint, if you don't specify it tests fail.
    res = client.post("/users/", json={"email" : "hubele@hebele.com", "password" : "hubele"})
    print(res.text)
    assert res.status_code == 201
    
def test_login():
    res = client.post("/login", data={"username" : "abov@abov.com", "password": "abov"})
    jwt = res.json().get("access_token")
    print(jwt)
    assert res.status_code == 200
    assert res.json().get("token_type") == "bearer"