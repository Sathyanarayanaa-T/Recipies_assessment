"""
Database connection and query utilities for Recipe API
"""
import sqlite3
import json
from pathlib import Path
from typing import Optional, Dict, Any, List, Tuple


# Database path - relative to project root
DB_PATH = Path(__file__).parent.parent.parent / "recipes.db"


def get_db_connection():
    """Create and return a database connection."""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row  # Enable column access by name
    return conn


def parse_nutrients(nutrients_json: str) -> Dict[str, Any]:
    """Parse nutrients JSON string into dictionary."""
    try:
        return json.loads(nutrients_json) if nutrients_json else {}
    except json.JSONDecodeError:
        return {}


def recipe_to_dict(row: sqlite3.Row) -> Dict[str, Any]:
    """Convert database row to recipe dictionary."""
    return {
        "id": row["id"],
        "cuisine": row["cuisine"],
        "title": row["title"],
        "rating": row["rating"],
        "prep_time": row["prep_time"],
        "cook_time": row["cook_time"],
        "total_time": row["total_time"],
        "description": row["description"],
        "nutrients": parse_nutrients(row["nutrients"]),
        "serves": row["serves"]
    }


def get_recipes_paginated(
    page: int = 1,
    limit: int = 10
) -> Tuple[List[Dict[str, Any]], int]:
    """
    Get paginated recipes sorted by rating descending.
    
    Args:
        page: Page number (1-indexed)
        limit: Number of recipes per page
    
    Returns:
        Tuple of (recipes list, total count)
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get total count
    cursor.execute("SELECT COUNT(*) as count FROM recipes")
    total_count = cursor.fetchone()["count"]
    
    # Get paginated recipes
    offset = (page - 1) * limit
    cursor.execute("""
        SELECT * FROM recipes
        ORDER BY rating DESC, id ASC
        LIMIT ? OFFSET ?
    """, (limit, offset))
    
    recipes = [recipe_to_dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return recipes, total_count


def search_recipes(
    page: int = 1,
    limit: int = 10,
    title: Optional[str] = None,
    cuisine: Optional[str] = None,
    rating: Optional[float] = None,
    total_time: Optional[int] = None,
    calories: Optional[int] = None
) -> Tuple[List[Dict[str, Any]], int]:
    """
    Search recipes with filters and pagination.
    
    Args:
        page: Page number (1-indexed)
        limit: Number of recipes per page
        title: Filter by title (case-insensitive partial match)
        cuisine: Filter by cuisine (case-insensitive partial match)
        rating: Minimum rating filter
        total_time: Maximum total time filter
        calories: Maximum calories filter
    
    Returns:
        Tuple of (recipes list, total count)
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Build WHERE clause dynamically
    where_clauses = []
    params = []
    
    if title:
        where_clauses.append("LOWER(title) LIKE LOWER(?)")
        params.append(f"%{title}%")
    
    if cuisine:
        where_clauses.append("LOWER(cuisine) LIKE LOWER(?)")
        params.append(f"%{cuisine}%")
    
    if rating is not None:
        where_clauses.append("rating >= ?")
        params.append(rating)
    
    if total_time is not None:
        where_clauses.append("total_time <= ?")
        params.append(total_time)
    
    # For calories, we need to filter on the nutrients JSON
    # SQLite doesn't have native JSONB, so we use string matching
    if calories is not None:
        where_clauses.append("""
            (nutrients LIKE '%"calories"%' AND 
             CAST(REPLACE(REPLACE(json_extract(nutrients, '$.calories'), ' kcal', ''), ' ', '') AS INTEGER) <= ?)
        """)
        params.append(calories)
    
    where_clause = " AND ".join(where_clauses) if where_clauses else "1=1"
    
    # Get total count with filters
    count_query = f"SELECT COUNT(*) as count FROM recipes WHERE {where_clause}"
    cursor.execute(count_query, params)
    total_count = cursor.fetchone()["count"]
    
    # Get paginated and filtered recipes
    offset = (page - 1) * limit
    query = f"""
        SELECT * FROM recipes
        WHERE {where_clause}
        ORDER BY rating DESC, id ASC
        LIMIT ? OFFSET ?
    """
    cursor.execute(query, params + [limit, offset])
    
    recipes = [recipe_to_dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return recipes, total_count
