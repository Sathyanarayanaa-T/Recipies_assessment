"""
Pydantic models for Recipe API
"""
from typing import Optional, Dict, Any, List
from pydantic import BaseModel


class Recipe(BaseModel):
    """Recipe model matching database schema."""
    id: int
    cuisine: Optional[str] = None
    title: str
    rating: Optional[float] = None
    prep_time: Optional[int] = None
    cook_time: Optional[int] = None
    total_time: Optional[int] = None
    description: Optional[str] = None
    nutrients: Dict[str, Any] = {}
    serves: Optional[str] = None


class PaginatedRecipeResponse(BaseModel):
    """Paginated response model for recipe endpoints."""
    page: int
    limit: int
    total_recipes: int
    total_pages: int
    recipes: List[Recipe]
