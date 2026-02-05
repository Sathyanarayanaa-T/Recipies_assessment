"""
Recipe Management API (Flask)
RESTful API for recipe search, retrieval, and management
"""
from flask import Flask, jsonify, request
from flask_cors import CORS
import math

from app.database.queries import get_recipes_paginated, search_recipes


app = Flask(__name__)
CORS(app)  # Enable CORS for all routes


@app.route('/', methods=['GET'])
def root():
    """API health check endpoint."""
    return jsonify({
        "message": "Recipe Management API",
        "status": "running",
        "version": "1.0.0",
        "endpoints": {
            "recipes": "/api/recipes",
            "search": "/api/recipes/search"
        }
    })


@app.route('/api/recipes', methods=['GET'])
def get_recipes():
    """
    Get all recipes with pagination, sorted by rating descending.
    
    Query Parameters:
    - page: Page number (default: 1)
    - limit: Results per page (default: 10, max: 100)
    """
    try:
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
        
        # Validate parameters
        if page < 1:
            return jsonify({"error": "Page must be >= 1"}), 400
        if limit < 1 or limit > 100:
            return jsonify({"error": "Limit must be between 1 and 100"}), 400
        
        recipes, total_count = get_recipes_paginated(page=page, limit=limit)
        total_pages = math.ceil(total_count / limit) if total_count > 0 else 0
        
        return jsonify({
            "page": page,
            "limit": limit,
            "total_recipes": total_count,
            "total_pages": total_pages,
            "recipes": recipes
        })
    except ValueError:
        return jsonify({"error": "Invalid parameters"}), 400
    except Exception as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500


@app.route('/api/recipes/search', methods=['GET'])
def search_recipes_endpoint():
    """
    Search recipes with multiple filters.
    
    Query Parameters:
    - title: Text search in recipe title
    - cuisine: Filter by cuisine type
    - rating: Minimum rating (0-5)
    - total_time: Maximum total time in minutes
    - calories: Maximum calories
    - page: Page number (default: 1)
    - limit: Results per page (default: 10, max: 100)
    """
    try:
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
        title = request.args.get('title')
        cuisine = request.args.get('cuisine')
        rating = request.args.get('rating')
        total_time = request.args.get('total_time')
        calories = request.args.get('calories')
        
        # Convert to appropriate types
        rating = float(rating) if rating else None
        total_time = int(total_time) if total_time else None
        calories = int(calories) if calories else None
        
        # Validate parameters
        if page < 1:
            return jsonify({"error": "Page must be >= 1"}), 400
        if limit < 1 or limit > 100:
            return jsonify({"error": "Limit must be between 1 and 100"}), 400
        if rating is not None and (rating < 0 or rating > 5):
            return jsonify({"error": "Rating must be between 0 and 5"}), 400
        
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
        
        return jsonify({
            "page": page,
            "limit": limit,
            "total_recipes": total_count,
            "total_pages": total_pages,
            "recipes": recipes
        })
    except ValueError as e:
        return jsonify({"error": f"Invalid parameters: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001, debug=True)
