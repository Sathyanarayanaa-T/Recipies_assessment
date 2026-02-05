"""
Pytest configuration and fixtures for API tests.
"""
import pytest
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.main import app


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def sample_recipe_data():
    """Sample recipe data for testing."""
    return {
        "id": 1,
        "cuisine": "Italian",
        "title": "Test Pasta",
        "rating": 4.5,
        "prep_time": 10,
        "cook_time": 20,
        "total_time": 30,
        "description": "A test pasta recipe",
        "nutrients": {"calories": "400 kcal", "protein": "15 g"},
        "serves": "4"
    }
