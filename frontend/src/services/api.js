/**
 * API Service for Recipe Management
 * Handles all API calls to the Flask backend
 */

const API_BASE_URL = 'http://localhost:8001/api';

/**
 * Fetch paginated recipes sorted by rating
 * @param {number} page - Page number (1-indexed)
 * @param {number} limit - Results per page
 * @returns {Promise<Object>} Response with recipes and pagination info
 */
export const getRecipes = async (page = 1, limit = 15) => {
    try {
        const response = await fetch(`${API_BASE_URL}/recipes?page=${page}&limit=${limit}`);
        if (!response.ok) {
            throw new Error(`API error: ${response.statusText}`);
        }
        return await response.json();
    } catch (error) {
        console.error('Error fetching recipes:', error);
        throw error;
    }
};

/**
 * Search recipes with filters
 * @param {Object} filters - Filter parameters
 * @param {number} page - Page number
 * @param {number} limit - Results per page
 * @returns {Promise<Object>} Filtered recipes with pagination info
 */
export const searchRecipes = async (filters = {}, page = 1, limit = 15) => {
    try {
        const params = new URLSearchParams();
        params.append('page', page);
        params.append('limit', limit);

        // Add filters if they exist
        if (filters.title) params.append('title', filters.title);
        if (filters.cuisine) params.append('cuisine', filters.cuisine);
        if (filters.rating) params.append('rating', filters.rating);
        if (filters.total_time) params.append('total_time', filters.total_time);
        if (filters.calories) params.append('calories', filters.calories);

        const response = await fetch(`${API_BASE_URL}/recipes/search?${params.toString()}`);
        if (!response.ok) {
            throw new Error(`API error: ${response.statusText}`);
        }
        return await response.json();
    } catch (error) {
        console.error('Error searching recipes:', error);
        throw error;
    }
};

/**
 * Fetch recipes (with or without filters)
 * @param {Object} filters - Filter parameters (optional)
 * @param {number} page - Page number
 * @param {number} limit - Results per page
 * @returns {Promise<Object>} Recipes with pagination info
 */
export const fetchRecipes = async (filters = {}, page = 1, limit = 15) => {
    const hasFilters = Object.values(filters).some(value => value && value !== '');

    if (hasFilters) {
        return searchRecipes(filters, page, limit);
    } else {
        return getRecipes(page, limit);
    }
};
