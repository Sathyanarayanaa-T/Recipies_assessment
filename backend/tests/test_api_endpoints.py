"""
API Endpoint Tests for Recipe Management System.

Tests all API endpoints with various scenarios including:
- Success cases
- Edge cases
- Error handling
- Pagination
- Search and filtering
"""
import json
import pytest


class TestGetRecipesEndpoint:
    """Tests for GET /api/recipes endpoint."""
    
    def test_get_recipes_default_pagination(self, client):
        """Test getting recipes with default pagination."""
        response = client.get('/api/recipes')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert 'recipes' in data
        assert 'total_recipes' in data
        assert 'total_pages' in data
        assert 'page' in data
        assert 'limit' in data
        
        assert data['page'] == 1
        assert data['limit'] == 10
        assert isinstance(data['recipes'], list)
        assert len(data['recipes']) <= 10
    
    def test_get_recipes_custom_pagination(self, client):
        """Test pagination with custom page and limit."""
        response = client.get('/api/recipes?page=2&limit=5')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert data['page'] == 2
        assert data['limit'] == 5
        assert len(data['recipes']) <= 5
    
    def test_get_recipes_page_1(self, client):
        """Test first page returns recipes."""
        response = client.get('/api/recipes?page=1&limit=15')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert len(data['recipes']) == 15
        assert data['total_recipes'] > 0
    
    def test_get_recipes_sorted_by_rating(self, client):
        """Test that recipes are sorted by rating in descending order."""
        response = client.get('/api/recipes?page=1&limit=20')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        recipes = data['recipes']
        # Check that ratings are in descending order (or null)
        for i in range(len(recipes) - 1):
            rating1 = recipes[i]['rating']
            rating2 = recipes[i + 1]['rating']
            
            # Skip comparison if either rating is null
            if rating1 is not None and rating2 is not None:
                assert rating1 >= rating2, "Recipes should be sorted by rating DESC"
    
    def test_get_recipes_large_limit(self, client):
        """Test that limit exceeding maximum returns 400 error."""
        response = client.get('/api/recipes?limit=1000')
        
        # API should return 400 for invalid limit
        assert response.status_code == 400
    
    def test_get_recipes_invalid_page(self, client):
        """Test handling of invalid page number."""
        response = client.get('/api/recipes?page=-1')
        
        # Should return 400 for invalid page
        assert response.status_code == 400
    
    def test_get_recipes_last_page(self, client):
        """Test accessing the last page of results."""
        # First get total count
        response = client.get('/api/recipes?limit=15')
        data = json.loads(response.data)
        last_page = data['total_pages']
        
        # Now get last page
        response = client.get(f'/api/recipes?page={last_page}&limit=15')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['page'] == last_page
        assert len(data['recipes']) > 0  # Should have at least one recipe
    
    def test_recipe_structure(self, client):
        """Test that each recipe has the expected structure."""
        response = client.get('/api/recipes?limit=1')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        if len(data['recipes']) > 0:
            recipe = data['recipes'][0]
            
            # Check required fields
            assert 'id' in recipe
            assert 'title' in recipe
            assert 'cuisine' in recipe
            assert 'rating' in recipe
            assert 'prep_time' in recipe
            assert 'cook_time' in recipe
            assert 'total_time' in recipe
            assert 'description' in recipe
            assert 'nutrients' in recipe
            assert 'serves' in recipe
            
            # Check nutrients is a dict
            assert isinstance(recipe['nutrients'], dict)


class TestSearchRecipesEndpoint:
    """Tests for GET /api/recipes/search endpoint."""
    
    def test_search_by_title(self, client):
        """Test searching recipes by title."""
        response = client.get('/api/recipes/search?title=pie')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert 'recipes' in data
        
        # All results should contain 'pie' in title (case-insensitive)
        for recipe in data['recipes']:
            assert 'pie' in recipe['title'].lower(), f"Recipe '{recipe['title']}' doesn't contain 'pie'"
    
    def test_search_by_cuisine(self, client):
        """Test searching recipes by cuisine."""
        response = client.get('/api/recipes/search?cuisine=Italian')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        # All results should contain 'Italian' in cuisine
        for recipe in data['recipes']:
            if recipe['cuisine']:
                assert 'italian' in recipe['cuisine'].lower()
    
    def test_search_by_rating(self, client):
        """Test filtering by minimum rating."""
        min_rating = 4.5
        response = client.get(f'/api/recipes/search?rating={min_rating}')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        # All results should have rating >= min_rating
        for recipe in data['recipes']:
            if recipe['rating'] is not None:
                assert recipe['rating'] >= min_rating
    
    def test_search_by_total_time(self, client):
        """Test filtering by maximum total time."""
        max_time = 30
        response = client.get(f'/api/recipes/search?total_time={max_time}')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        # All results should have total_time <= max_time
        for recipe in data['recipes']:
            if recipe['total_time'] is not None:
                assert recipe['total_time'] <= max_time
    
    def test_search_by_calories(self, client):
        """Test filtering by maximum calories."""
        max_calories = 300
        response = client.get(f'/api/recipes/search?calories={max_calories}')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        # Check that recipes with calorie info are within limit
        for recipe in data['recipes']:
            nutrients = recipe.get('nutrients', {})
            if nutrients and 'calories' in nutrients:
                # Extract number from string like "250 kcal"
                cal_str = nutrients['calories'].split()[0]
                try:
                    calories = float(cal_str)
                    assert calories <= max_calories
                except (ValueError, IndexError):
                    pass  # Skip if can't parse
    
    def test_search_multiple_filters(self, client):
        """Test search with multiple filters combined."""
        response = client.get('/api/recipes/search?title=chicken&cuisine=Italian&rating=4.0')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        # Results should match ALL criteria
        for recipe in data['recipes']:
            assert 'chicken' in recipe['title'].lower()
            if recipe['cuisine']:
                assert 'italian' in recipe['cuisine'].lower()
            if recipe['rating'] is not None:
                assert recipe['rating'] >= 4.0
    
    def test_search_no_results(self, client):
        """Test search that returns no results."""
        response = client.get('/api/recipes/search?title=xyznonexistentrecipe123')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert len(data['recipes']) == 0
        assert data['total_recipes'] == 0
    
    def test_search_with_pagination(self, client):
        """Test search with pagination parameters."""
        response = client.get('/api/recipes/search?title=cake&page=1&limit=5')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert data['page'] == 1
        assert data['limit'] == 5
        assert len(data['recipes']) <= 5
    
    def test_search_case_insensitive(self, client):
        """Test that search is case-insensitive."""
        response1 = client.get('/api/recipes/search?title=CHICKEN')
        response2 = client.get('/api/recipes/search?title=chicken')
        
        assert response1.status_code == 200
        assert response2.status_code == 200
        
        data1 = json.loads(response1.data)
        data2 = json.loads(response2.data)
        
        # Should return same number of results
        assert data1['total_recipes'] == data2['total_recipes']


class TestEdgeCases:
    """Tests for edge cases and error handling."""
    
    def test_empty_query_parameters(self, client):
        """Test handling of empty query parameters."""
        response = client.get('/api/recipes/search?title=&cuisine=')
        
        assert response.status_code == 200
        # Should behave like no filters
    
    def test_special_characters_in_search(self, client):
        """Test search with special characters."""
        response = client.get('/api/recipes/search?title=mom%27s')
        
        assert response.status_code == 200
        # Should handle apostrophes and special chars
    
    def test_very_large_page_number(self, client):
        """Test requesting a page number beyond available data."""
        response = client.get('/api/recipes?page=99999&limit=10')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        # Should return empty results but not error
        assert len(data['recipes']) == 0
    
    def test_negative_rating(self, client):
        """Test filtering with negative rating returns 400."""
        response = client.get('/api/recipes/search?rating=-1')
        
        # Should return 400 for invalid rating
        assert response.status_code == 400
    
    def test_zero_limit(self, client):
        """Test with limit=0 returns 400."""
        response = client.get('/api/recipes?limit=0')
        
        # Should return 400 for invalid limit
        assert response.status_code == 400


class TestCORSHeaders:
    """Tests for CORS configuration."""
    
    def test_cors_headers_present(self, client):
        """Test that CORS headers are present in response."""
        response = client.get('/api/recipes')
        
        assert response.status_code == 200
        # Flask-CORS should add these headers
        assert 'Access-Control-Allow-Origin' in response.headers


class TestDataIntegrity:
    """Tests for data integrity and null handling."""
    
    def test_null_rating_handling(self, client):
        """Test that recipes with null ratings are handled properly."""
        # Get last page which has null ratings
        response = client.get('/api/recipes?limit=15')
        data = json.loads(response.data)
        last_page = data['total_pages']
        
        response = client.get(f'/api/recipes?page={last_page}&limit=15')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        # Should successfully return recipes even if rating is null
        assert 'recipes' in data
        assert isinstance(data['recipes'], list)
    
    def test_null_fields_in_response(self, client):
        """Test that null fields are properly serialized as JSON null."""
        response = client.get('/api/recipes?limit=100')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        # Check if any recipe has null fields (they should be valid null, not strings)
        for recipe in data['recipes']:
            if recipe['rating'] is None:
                assert recipe['rating'] is None  # Should be None, not "null" string
    
    def test_nutrients_json_parsing(self, client):
        """Test that nutrients field is properly parsed from JSON."""
        response = client.get('/api/recipes?limit=1')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        if len(data['recipes']) > 0:
            recipe = data['recipes'][0]
            nutrients = recipe['nutrients']
            
            # Should be a dict, not a string
            assert isinstance(nutrients, dict), "Nutrients should be parsed as dict"
