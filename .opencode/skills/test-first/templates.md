# Templates

```python
import pytest
from dice_api.dice import parse

@pytest.mark.parametrize("expr, fragment", [("0d6", "at least 1"), ("abc", "invalid")])
def test_invalid(expr, fragment):
    with pytest.raises(ValueError) as e:
        parse(expr)
    assert fragment in str(e.value)
```

```python
from fastapi.testclient import TestClient
from dice_api.main import app

client = TestClient(app)

def test_endpoint():
    r = client.get("/roll", params={"expr": "d20", "seed": 1})
    assert r.status_code == 200
    assert r.json()["total"] == r.json()["rolls"][0]
```
