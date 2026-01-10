"""Pytest configuration for Ada1Status tests."""
import pytest
from unittest.mock import MagicMock

# Mock Home Assistant core for testing
pytest_plugins = "pytest_homeassistant_custom_component"


@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(enable_custom_integrations):
    """Enable custom integrations for all tests."""
    yield
