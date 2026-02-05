"""
Recipe API Routes
"""
from fastapi import APIRouter, Query, HTTPException
from typing import Optional
import math

from app.models.recipe import PaginatedRecipeResponse, Recipe
from app.database.queries import get_recipes_paginated, search_recipes


router = APIRouter(prefix="/api", tags=["recipes"])


@router.get("/recipes", response_model=PaginatedRecipeResponse)
async def get_recipes(
    page: int = Query(1, ge=1, description="Page number (starting from 1)"),
    limit: int = Query(10, ge=1, le=100, description="Number of recipes per page")
):
    """
    Get all recipes with pagination, sorted by rating descending.
    
    Parameters:
    - **page**: Page number (default: 1)
    - **limit**: Results per page (default: 10, max: 100)
    
    Returns:
    - Paginated list of recipes sorted by rating (highest first)
    """
    try:
        recipes, total_count = get_recipes_paginated(page=page, limit=limit)
        total_pages = math.ceil(total_count / limit) if total_count > 0 else 0
        
        return PaginatedRecipeResponse(
            page=page,
            limit=limit,
            total_recipes=total_count,
            total_pages=total_pages,
            recipes=recipes
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.get("/recipes/search", response_model=PaginatedRecipeResponse)
async def search_recipes_endpoint(
    page: int = Query(1, ge=1, description="Page number (starting from 1)"),
    limit: int = Query(10, ge=1, le=100, description="Number of recipes per page"),
    title: Optional[str] = Query(None, description="Search in recipe title (case-insensitive)"),
    cuisine: Optional[str] = Query(None, description="Filter by cuisine type"),
    rating: Optional[float] = Query(None, ge=0, le=5, description="Minimum rating filter"),
    total_time: Optional[int] = Query(None, ge=0, description="Maximum total time in minutes"),
    calories: Optional[int] = Query(None, ge=0, description="Maximum calories")
):
    """
    Search recipes with multiple filters.
    
    **Filters** (all optional, combined with AND logic):
    - **title**: Text search in recipe title
    - **cuisine**: Filter by cuisine type
    - **rating**: Minimum rating (0-5)
    - **total_time**: Maximum total time in minutes
    - **calories**: Maximum calories
    
    **Pagination**:
    - **page**: Page number (default: 1)
    - **limit**: Results per page (default: 10, max: 100)
    
    Returns:
    - Paginated list of filtered recipes sorted by rating (highest first)
    """
    try:
        recipes, total_count = search_recipes(
            page=page,
            limit=limit,
            title=title,
            cuisine=cuisine,
            rating=rating,
            total_time=total_time,
            calories=calories
        )
        
        total_pages = math.ceil(total_count / limit) if total_count > 0 else 0
        
        return PaginatedRecipeResponse(
            page=page,
            limit=limit,
            total_recipes=total_count,
            total_pages=total_pages,
            recipes=recipes
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
