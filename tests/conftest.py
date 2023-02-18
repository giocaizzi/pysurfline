"""conftest pytest"""

import pytest
import json

@pytest.fixture
def cached_json():
    """gets cached json responses from tests/fixtures folder"""
    with open(f"tests/fixtures/surf.json", "r") as f:
        return json.load(f)