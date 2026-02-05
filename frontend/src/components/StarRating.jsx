import React from 'react';

const StarRating = ({ rating }) => {
    const fullStars = Math.floor(rating);
    const hasHalfStar = rating % 1 >= 0.5;
    const emptyStars = 5 - fullStars - (hasHalfStar ? 1 : 0);

    return (
        <div className="flex items-center gap-1">
            {/* Full Stars */}
            {[...Array(fullStars)].map((_, i) => (
                <svg
                    key={`full-${i}`}
                    className="w-5 h-5 text-yellow-400 fill-current"
                    viewBox="0 0 20 20"
                >
                    <path d="M10 15l-5.878 3.09 1.123-6.545L.489 6.91l6.572-.955L10 0l2.939 5.955 6.572.955-4.756 4.635 1.123 6.545z" />
                </svg>
            ))}

            {/* Half Star */}
            {hasHalfStar && (
                <svg
                    className="w-5 h-5 text-yellow-400"
                    viewBox="0 0 20 20"
                >
                    <defs>
                        <linearGradient id="half">
                            <stop offset="50%" stopColor="currentColor" />
                            <stop offset="50%" stopColor="#e5e7eb" />
                        </linearGradient>
                    </defs>
                    <path
                        fill="url(#half)"
                        d="M10 15l-5.878 3.09 1.123-6.545L.489 6.91l6.572-.955L10 0l2.939 5.955 6.572.955-4.756 4.635 1.123 6.545z"
                    />
                </svg>
            )}

            {/* Empty Stars */}
            {[...Array(emptyStars)].map((_, i) => (
                <svg
                    key={`empty-${i}`}
                    className="w-5 h-5 text-gray-300 fill-current"
                    viewBox="0 0 20 20"
                >
                    <path d="M10 15l-5.878 3.09 1.123-6.545L.489 6.91l6.572-.955L10 0l2.939 5.955 6.572.955-4.756 4.635 1.123 6.545z" />
                </svg>
            ))}

            <span className="ml-2 text-sm font-medium text-slate-700">{rating.toFixed(1)}</span>
        </div>
    );
};

export default StarRating;
