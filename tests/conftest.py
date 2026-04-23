from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

from src import app as app_module


BASELINE_ACTIVITIES = deepcopy(app_module.activities)


@pytest.fixture(autouse=True)
def reset_activities(monkeypatch):
    # Keep tests deterministic by restoring in-memory backend state per test.
    monkeypatch.setattr(app_module, "activities", deepcopy(BASELINE_ACTIVITIES))


@pytest.fixture
def client(reset_activities):
    return TestClient(app_module.app)
