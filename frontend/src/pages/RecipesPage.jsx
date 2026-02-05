import React, { useState, useEffect } from 'react';
import RecipeTable from '../components/RecipeTable';
import RecipeDetailDrawer from '../components/RecipeDetailDrawer';
import SearchFilters from '../components/SearchFilters';
import PaginationControls from '../components/PaginationControls';
import NoResults from '../components/NoResults';
import { fetchRecipes } from '../services/api';

const RecipesPage = () => {
    const [selectedRecipe, setSelectedRecipe] = useState(null);
    const [isDrawerOpen, setIsDrawerOpen] = useState(false);
    const [currentPage, setCurrentPage] = useState(1);
    const [limit, setLimit] = useState(15);
    const [filters, setFilters] = useState({});
    const [recipeData, setRecipeData] = useState(null);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);

    useEffect(() => {
        const loadRecipes = async () => {
            setIsLoading(true);
            setError(null);

            const startTime = Date.now();

            try {
                const data = await fetchRecipes(filters, currentPage, limit);

                // Ensure minimum loading time for smooth animations (300ms)
                const elapsedTime = Date.now() - startTime;
                const minLoadingTime = 300;

                if (elapsedTime < minLoadingTime) {
                    await new Promise(resolve => setTimeout(resolve, minLoadingTime - elapsedTime));
                }

                setRecipeData(data);
            } catch (err) {
                console.error('Failed to load recipes:', err);
                setError('Failed to load recipes. Please make sure the API server is running.');
            } finally {
                setIsLoading(false);
            }
        };

        loadRecipes();
    }, [currentPage, limit, filters]);

    const handleRecipeClick = (recipe) => {
        setSelectedRecipe(recipe);
        setIsDrawerOpen(true);
    };

    const handleFilterChange = (newFilters) => {
        setFilters(newFilters);
        setCurrentPage(1); // Reset to first page on filter change
    };

    const handleClearFilters = () => {
        setFilters({});
        setCurrentPage(1);
    };

    const handlePageChange = (page) => {
        setCurrentPage(page);
        window.scrollTo({ top: 0, behavior: 'smooth' });
    };

    const handleLimitChange = (newLimit) => {
        setLimit(newLimit);
        setCurrentPage(1); // Reset to first page on limit change
    };

    const hasFilters = Object.values(filters).some(value => value !== '');
    const hasRecipes = recipeData && recipeData.recipes.length > 0;

    return (
        <div className="min-h-screen bg-gradient-to-br from-slate-50 via-primary-50 to-slate-50">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                {/* Header */}
                <div className="mb-8">
                    <h1 className="text-4xl font-bold text-slate-900 mb-2">
                        Recipe Collection
                    </h1>
                    <p className="text-slate-600">
                        Discover delicious recipes from around the world
                    </p>
                </div>

                {/* Search Filters */}
                <SearchFilters
                    onFilterChange={handleFilterChange}
                    onClearFilters={handleClearFilters}
                />

                {/* Error Message */}
                {error && (
                    <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
                        <p className="text-red-800 text-sm">{error}</p>
                    </div>
                )}

                {/* Loading State */}
                {isLoading && (
                    <RecipeTable
                        recipes={[]}
                        onRecipeClick={() => { }}
                        isLoading={true}
                    />
                )}

                {/* Recipe Table with Results */}
                {!isLoading && hasRecipes && (
                    <>
                        <RecipeTable
                            recipes={recipeData.recipes}
                            onRecipeClick={handleRecipeClick}
                            isLoading={false}
                        />

                        <PaginationControls
                            currentPage={currentPage}
                            totalPages={recipeData.total_pages}
                            totalRecipes={recipeData.total_recipes}
                            limit={limit}
                            onPageChange={handlePageChange}
                            onLimitChange={handleLimitChange}
                        />
                    </>
                )}

                {/* No Results - With Filters */}
                {!isLoading && !hasRecipes && hasFilters && !error && (
                    <NoResults type="search" />
                )}

                {/* No Results - Without Filters */}
                {!isLoading && !hasRecipes && !hasFilters && !error && (
                    <NoResults type="noData" />
                )}
            </div>

            {/* Recipe Detail Drawer */}
            <RecipeDetailDrawer
                recipe={selectedRecipe}
                isOpen={isDrawerOpen}
                onClose={() => setIsDrawerOpen(false)}
            />
        </div>
    );
};

export default RecipesPage;
