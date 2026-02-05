import React from 'react';
import RecipeRow from './RecipeRow';

const RecipeTable = ({ recipes, onRecipeClick, isLoading }) => {
    if (isLoading) {
        return (
            <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
                <div className="animate-pulse">
                    {[...Array(5)].map((_, i) => (
                        <div key={i} className="border-b border-slate-200 px-6 py-4">
                            <div className="flex items-center gap-4">
                                <div className="h-6 bg-slate-200 rounded w-1/3"></div>
                                <div className="h-6 bg-slate-200 rounded w-24"></div>
                                <div className="h-6 bg-slate-200 rounded w-32"></div>
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        );
    }

    return (
        <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
            <div className="overflow-x-auto">
                <table className="w-full">
                    <thead className="bg-gradient-to-r from-slate-50 to-slate-100 border-b border-slate-200">
                        <tr>
                            <th className="px-6 py-4 text-left text-xs font-semibold text-slate-700 uppercase tracking-wider">
                                Recipe Title
                            </th>
                            <th className="px-6 py-4 text-left text-xs font-semibold text-slate-700 uppercase tracking-wider">
                                Cuisine
                            </th>
                            <th className="px-6 py-4 text-left text-xs font-semibold text-slate-700 uppercase tracking-wider">
                                Rating
                            </th>
                            <th className="px-6 py-4 text-left text-xs font-semibold text-slate-700 uppercase tracking-wider">
                                Total Time
                            </th>
                            <th className="px-6 py-4 text-left text-xs font-semibold text-slate-700 uppercase tracking-wider">
                                Serves
                            </th>
                        </tr>
                    </thead>
                    <tbody>
                        {recipes.map((recipe) => (
                            <RecipeRow
                                key={recipe.id}
                                recipe={recipe}
                                onClick={onRecipeClick}
                            />
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default RecipeTable;
