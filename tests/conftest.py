import pytest
from fastapi.testclient import TestClient
from copy import deepcopy
import src.app as app_module


@pytest.fixture
def client():
    with TestClient(app_module.app) as c:
        yield c


@pytest.fixture(autouse=True)
def preserve_activities():
    original = deepcopy(app_module.activities)
    try:
        yield
    finally:
        app_module.activities.clear()
        app_module.activities.update(deepcopy(original))
