import pytest
from unittest.mock import patch, MagicMock
from src.data.client import ComptrollerClient
from src.data.resources import SalesTaxResource, FranchiseResource, MixedBeverageResource


def test_comptroller_client_factory(monkeypatch):
    with patch("src.data.client.SocrataClient") as MockSocrata:
        MockSocrata.return_value = object()
        client = ComptrollerClient.factory("dummy")
        assert isinstance(client, ComptrollerClient)
        assert client.socrata is not None


def test_sales_tax_returns_resource():
    with patch("src.data.client.SocrataClient") as MockSocrata:
        mock_socrata = MockSocrata.return_value
        client = ComptrollerClient("dummy")
        resource = client.sales_tax()
        assert isinstance(resource, SalesTaxResource)
        assert resource.client == mock_socrata


def test_franchise_tax_returns_resource():
    with patch("src.data.client.SocrataClient") as MockSocrata:
        mock_socrata = MockSocrata.return_value
        client = ComptrollerClient("dummy")
        resource = client.franchise_tax()
        assert isinstance(resource, FranchiseResource)
        assert resource.client == mock_socrata


def test_mixed_beverage_tax_returns_resource():
    with patch("src.data.client.SocrataClient") as MockSocrata:
        mock_socrata = MockSocrata.return_value
        client = ComptrollerClient("dummy")
        resource = client.mixed_beverage_tax()
        assert isinstance(resource, MixedBeverageResource)
        assert resource.client == mock_socrata


def test_get_delegates_to_socrata():
    with patch("src.data.client.SocrataClient") as MockSocrata:
        mock_socrata = MockSocrata.return_value
        mock_socrata.get.return_value = [{"id": 1}]
        client = ComptrollerClient("dummy")

        result = client.get("dataset123", {"$limit": 1})

        mock_socrata.get.assert_called_once_with("dataset123", {"$limit": 1})
        assert result == [{"id": 1}]
