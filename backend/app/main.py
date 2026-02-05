"""
Recipe Management API (Flask)
RESTful API for recipe search, retrieval, and management
"""
from flask import Flask, jsonify, request
from flask_cors import CORS
from flasgger import Swagger
import math

from app.database.queries import get_recipes_paginated, search_recipes


app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Swagger configuration
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs"
}

swagger_template = {
    "info": {
        "title": "Recipe Management API",
        "description": "API for browsing and searching 8,451+ recipes with advanced filtering",
        "version": "1.0.0",
        "contact": {
            "name": "Sathyanarayana T",
            "url": "https://github.com/Sathyanarayanaa-T/Recipies_assessment"
        }
    },
    "host": "localhost:8001",
    "basePath": "/",
    "schemes": ["http"]
}

Swagger(app, config=swagger_config, template=swagger_template)


@app.route('/', methods=['GET'])
def root():
    """
    API Health Check
    ---
    tags:
      - Health
    responses:
      200:
        description: API status and available endpoints
        schema:
          type: object
          properties:
            message:
              type: string
              example: Recipe Management API
            status:
              type: string
              example: running
            version:
              type: string
              example: 1.0.0
            endpoints:
              type: object
    """
    return jsonify({
        "message": "Recipe Management API",
        "status": "running",
        "version": "1.0.0",
        "endpoints": {
            "recipes": "/api/recipes",
            "search": "/api/recipes/search",
            "docs": "/apidocs"
        }
    })


@app.route('/api/recipes', methods=['GET'])
def get_recipes():
    """
    Get Paginated Recipes
    ---
    tags:
      - Recipes
    parameters:
      - name: page
        in: query
        type: integer
        required: false
        default: 1
        description: Page number (must be >= 1)
      - name: limit
        in: query
        type: integer
        required: false
        default: 10
        description: Results per page (1-100)
    responses:
      200:
        description: Paginated list of recipes sorted by rating (descending)
        schema:
          type: object
          properties:
            page:
              type: integer
              example: 1
            limit:
              type: integer
              example: 15
            total_recipes:
              type: integer
              example: 8451
            total_pages:
              type: integer
              example: 564
            recipes:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                  title:
                    type: string
                  cuisine:
                    type: string
                  rating:
                    type: number
                    nullable: true
                  prep_time:
                    type: integer
                    nullable: true
                  cook_time:
                    type: integer
                    nullable: true
                  total_time:
                    type: integer
                    nullable: true
                  description:
                    type: string
                  nutrients:
                    type: object
                  serves:
                    type: string
      400:
        description: Invalid parameters
        schema:
          type: object
          properties:
            error:
              type: string
      500:
        description: Server error
        schema:
          type: object
          properties:
            error:
              type: string
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
    Search Recipes with Filters
    ---
    tags:
      - Recipes
    parameters:
      - name: title
        in: query
        type: string
        required: false
        description: Search by recipe title (case-insensitive)
        example: pie
      - name: cuisine
        in: query
        type: string
        required: false
        description: Filter by cuisine type
        example: Italian
      - name: rating
        in: query
        type: number
        required: false
        description: Minimum rating (0-5)
        example: 4.5
      - name: total_time
        in: query
        type: integer
        required: false
        description: Maximum total time in minutes
        example: 30
      - name: calories
        in: query
        type: integer
        required: false
        description: Maximum calories
        example: 300
      - name: page
        in: query
        type: integer
        required: false
        default: 1
        description: Page number
      - name: limit
        in: query
        type: integer
        required: false
        default: 10
        description: Results per page (1-100)
    responses:
      200:
        description: Filtered and paginated list of recipes
        schema:
          type: object
          properties:
            page:
              type: integer
            limit:
              type: integer
            total_recipes:
              type: integer
            total_pages:
              type: integer
            recipes:
              type: array
              items:
                type: object
      400:
        description: Invalid parameters
        schema:
          type: object
          properties:
            error:
              type: string
      500:
        description: Server error
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
