import React, { useState } from 'react';

const RecipeDetailDrawer = ({ recipe, isOpen, onClose }) => {
    const [isTimeExpanded, setIsTimeExpanded] = useState(false);

    if (!isOpen || !recipe) return null;

    const nutrients = [
        { label: 'Calories', value: recipe.nutrients.calories },
        { label: 'Carbohydrates', value: recipe.nutrients.carbohydrateContent },
        { label: 'Cholesterol', value: recipe.nutrients.cholesterolContent },
        { label: 'Fiber', value: recipe.nutrients.fiberContent },
        { label: 'Protein', value: recipe.nutrients.proteinContent },
        { label: 'Saturated Fat', value: recipe.nutrients.saturatedFatContent },
        { label: 'Sugar', value: recipe.nutrients.sugarContent },
        { label: 'Fat', value: recipe.nutrients.fatContent },
        { label: 'Sodium', value: recipe.nutrients.sodiumContent },
    ];

    return (
        <>
            {/* Backdrop */}
            <div
                className="fixed inset-0 bg-black/30 backdrop-blur-sm z-40 transition-opacity"
                onClick={onClose}
            />

            {/* Drawer */}
            <div className="fixed right-0 top-0 h-full w-full md:w-[600px] bg-white shadow-2xl z-50 overflow-y-auto animate-slide-in">
                {/* Header */}
                <div className="sticky top-0 bg-white border-b border-slate-200 px-6 py-4 flex items-start justify-between">
                    <div className="flex-1 pr-4">
                        <h2 className="text-2xl font-bold text-slate-900 mb-1">{recipe.title}</h2>
                        <span className="inline-block px-3 py-1 bg-primary-100 text-primary-700 rounded-full text-sm font-medium">
                            {recipe.cuisine}
                        </span>
                    </div>
                    <button
                        onClick={onClose}
                        className="p-2 hover:bg-slate-100 rounded-lg transition-colors"
                    >
                        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                        </svg>
                    </button>
                </div>

                {/* Content */}
                <div className="p-6 space-y-6">
                    {/* Description */}
                    <div className="space-y-2">
                        <h3 className="text-sm font-semibold text-slate-500 uppercase tracking-wide">Description</h3>
                        <p className="text-slate-700 leading-relaxed">{recipe.description}</p>
                    </div>

                    {/* Serves */}
                    <div className="flex items-center gap-2 text-slate-700">
                        <svg className="w-5 h-5 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                        </svg>
                        <span className="font-medium">{recipe.serves}</span>
                    </div>

                    {/* Time Information */}
                    <div className="space-y-2">
                        <h3 className="text-sm font-semibold text-slate-500 uppercase tracking-wide">Time</h3>
                        <div className="bg-slate-50 rounded-lg p-4">
                            <button
                                onClick={() => setIsTimeExpanded(!isTimeExpanded)}
                                className="w-full flex items-center justify-between group"
                            >
                                <div className="flex items-center gap-2">
                                    <svg className="w-5 h-5 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                                    </svg>
                                    <span className="font-medium text-slate-900">Total Time: {recipe.total_time} minutes</span>
                                </div>
                                <svg
                                    className={`w-5 h-5 text-slate-400 transition-transform ${isTimeExpanded ? 'rotate-180' : ''}`}
                                    fill="none"
                                    stroke="currentColor"
                                    viewBox="0 0 24 24"
                                >
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                                </svg>
                            </button>

                            {isTimeExpanded && (
                                <div className="mt-4 ml-7 space-y-2 border-l-2 border-primary-300 pl-4">
                                    <div className="flex items-center gap-2 text-slate-700">
                                        <span className="text-sm">Prep Time:</span>
                                        <span className="font-medium">{recipe.prep_time} minutes</span>
                                    </div>
                                    <div className="flex items-center gap-2 text-slate-700">
                                        <span className="text-sm">Cook Time:</span>
                                        <span className="font-medium">{recipe.cook_time} minutes</span>
                                    </div>
                                </div>
                            )}
                        </div>
                    </div>

                    {/* Nutritional Information */}
                    <div className="space-y-3">
                        <h3 className="text-sm font-semibold text-slate-500 uppercase tracking-wide">Nutritional Information</h3>
                        <div className="bg-slate-50 rounded-lg overflow-hidden">
                            <table className="w-full">
                                <thead className="bg-slate-100">
                                    <tr>
                                        <th className="px-4 py-3 text-left text-xs font-semibold text-slate-700 uppercase">Nutrient</th>
                                        <th className="px-4 py-3 text-right text-xs font-semibold text-slate-700 uppercase">Amount</th>
                                    </tr>
                                </thead>
                                <tbody className="divide-y divide-slate-200">
                                    {nutrients.map((nutrient, index) => (
                                        <tr key={index} className="hover:bg-white transition-colors">
                                            <td className="px-4 py-3 text-sm text-slate-700">{nutrient.label}</td>
                                            <td className="px-4 py-3 text-sm font-medium text-slate-900 text-right">{nutrient.value}</td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>

            <style>{`
        @keyframes slide-in {
          from {
            transform: translateX(100%);
          }
          to {
            transform: translateX(0);
          }
        }
        
        .animate-slide-in {
          animation: slide-in 0.3s ease-out;
        }
      `}</style>
        </>
    );
};

export default RecipeDetailDrawer;
