import React from 'react';
import StarRating from './StarRating';

const RecipeRow = ({ recipe, onClick, index = 0 }) => {
    const truncateTitle = (title, maxLength = 50) => {
        // Handle null or undefined title
        if (!title) return 'Untitled Recipe';
        return title.length > maxLength ? title.substring(0, maxLength) + '...' : title;
    };

    // Calculate stagger delay for smooth reveal (max 150ms)
    const animationDelay = `${Math.min(index * 30, 150)}ms`;

    return (
        <tr
            onClick={() => onClick(recipe)}
            className="border-b border-slate-200 hover:bg-primary-50 cursor-pointer transition-colors group animate-slideIn"
            style={{ animationDelay }}
        >
            <td className="px-6 py-4">
                <div className="flex items-center gap-2">
                    <span
                        className="text-slate-900 font-medium group-hover:text-primary-700 transition-colors"
                        title={recipe.title || 'Untitled Recipe'}
                    >
                        {truncateTitle(recipe.title)}
                    </span>
                </div>
            </td>
            <td className="px-6 py-4">
                <span className="inline-block px-3 py-1 bg-slate-100 text-slate-700 rounded-full text-sm font-medium">
                    {recipe.cuisine || 'Unknown'}
                </span>
            </td>
            <td className="px-6 py-4">
                <StarRating rating={recipe.rating} />
            </td>
            <td className="px-6 py-4">
                <div className="flex items-center gap-2 text-slate-700">
                    <svg className="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    <span>{recipe.total_time ? `${recipe.total_time} min` : 'N/A'}</span>
                </div>
            </td>
            <td className="px-6 py-4">
                <div className="flex items-center gap-2 text-slate-700">
                    <svg className="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                    </svg>
                    <span>{recipe.serves || 'N/A'}</span>
                </div>
            </td>
        </tr>
    );
};

export default RecipeRow;
