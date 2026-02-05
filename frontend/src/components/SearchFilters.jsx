import React, { useState } from 'react';

const SearchFilters = ({ onFilterChange, onClearFilters }) => {
    const [isExpanded, setIsExpanded] = useState(true);
    const [filters, setFilters] = useState({
        title: '',
        cuisine: '',
        calories: '',
        total_time: '',
        rating: ''
    });

    const handleChange = (field, value) => {
        const newFilters = { ...filters, [field]: value };
        setFilters(newFilters);
        onFilterChange(newFilters);
    };

    const handleClear = () => {
        const clearedFilters = {
            title: '',
            cuisine: '',
            calories: '',
            total_time: '',
            rating: ''
        };
        setFilters(clearedFilters);
        onClearFilters();
    };

    const hasActiveFilters = Object.values(filters).some(value => value !== '');

    return (
        <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden mb-6">
            {/* Header */}
            <div className="px-6 py-4 bg-gradient-to-r from-primary-50 to-primary-100 flex items-center justify-between">
                <div className="flex items-center gap-2">
                    <svg className="w-5 h-5 text-primary-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
                    </svg>
                    <h3 className="font-semibold text-slate-900">Search & Filter Recipes</h3>
                    {hasActiveFilters && (
                        <span className="px-2 py-1 bg-primary-600 text-white text-xs rounded-full">
                            Active
                        </span>
                    )}
                </div>
                <button
                    onClick={() => setIsExpanded(!isExpanded)}
                    className="p-1 hover:bg-primary-200 rounded transition-colors"
                >
                    <svg
                        className={`w-5 h-5 text-primary-700 transition-transform ${isExpanded ? 'rotate-180' : ''}`}
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                    >
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                    </svg>
                </button>
            </div>

            {/* Filter Form */}
            {isExpanded && (
                <div className="p-6">
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-4">
                        {/* Title Search */}
                        <div>
                            <label htmlFor="title" className="block text-sm font-medium text-slate-700 mb-2">
                                Recipe Name
                            </label>
                            <input
                                id="title"
                                type="text"
                                value={filters.title}
                                onChange={(e) => handleChange('title', e.target.value)}
                                placeholder="Search by title..."
                                className="input"
                            />
                        </div>

                        {/* Cuisine Filter */}
                        <div>
                            <label htmlFor="cuisine" className="block text-sm font-medium text-slate-700 mb-2">
                                Cuisine Type
                            </label>
                            <input
                                id="cuisine"
                                type="text"
                                value={filters.cuisine}
                                onChange={(e) => handleChange('cuisine', e.target.value)}
                                placeholder="e.g., Italian, Mexican..."
                                className="input"
                            />
                        </div>

                        {/* Rating Filter */}
                        <div>
                            <label htmlFor="rating" className="block text-sm font-medium text-slate-700 mb-2">
                                Minimum Rating
                            </label>
                            <div className="relative">
                                <input
                                    id="rating"
                                    type="number"
                                    min="0"
                                    max="5"
                                    step="0.1"
                                    value={filters.rating}
                                    onChange={(e) => handleChange('rating', e.target.value)}
                                    placeholder="e.g., 4.5"
                                    className="input pr-10"
                                />
                                <svg className="absolute right-3 top-1/2 -translate-y-1/2 w-5 h-5 text-yellow-400" fill="currentColor" viewBox="0 0 20 20">
                                    <path d="M10 15l-5.878 3.09 1.123-6.545L.489 6.91l6.572-.955L10 0l2.939 5.955 6.572.955-4.756 4.635 1.123 6.545z" />
                                </svg>
                            </div>
                        </div>

                        {/* Calories Filter */}
                        <div>
                            <label htmlFor="calories" className="block text-sm font-medium text-slate-700 mb-2">
                                Max Calories (kcal)
                            </label>
                            <input
                                id="calories"
                                type="number"
                                min="0"
                                value={filters.calories}
                                onChange={(e) => handleChange('calories', e.target.value)}
                                placeholder="e.g., 500"
                                className="input"
                            />
                        </div>

                        {/* Total Time Filter */}
                        <div>
                            <label htmlFor="total_time" className="block text-sm font-medium text-slate-700 mb-2">
                                Max Total Time (min)
                            </label>
                            <input
                                id="total_time"
                                type="number"
                                min="0"
                                value={filters.total_time}
                                onChange={(e) => handleChange('total_time', e.target.value)}
                                placeholder="e.g., 60"
                                className="input"
                            />
                        </div>
                    </div>

                    {/* Clear Button */}
                    {hasActiveFilters && (
                        <div className="flex justify-end">
                            <button
                                onClick={handleClear}
                                className="btn-secondary flex items-center gap-2"
                            >
                                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                                </svg>
                                Clear Filters
                            </button>
                        </div>
                    )}
                </div>
            )}
        </div>
    );
};

export default SearchFilters;
