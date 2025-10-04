import pytest

class DummyClient:
    """A fake client that returns predefined data."""
    def __init__(self, records):
        self._records = records
    def get(self, dataset_id, params=None):
        return self._records

@pytest.fixture
def dummy_client():
    return DummyClient
