import React from 'react';

const NoResults = ({ type = 'search' }) => {
    const messages = {
        search: {
            title: 'No Recipes Found',
            description: 'No recipes match your current filters. Try adjusting your search criteria.',
            icon: (
                <svg className="w-20 h-20 text-slate-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
            )
        },
        noData: {
            title: 'No Data Available',
            description: 'No recipes are available at the moment. Please try again later.',
            icon: (
                <svg className="w-20 h-20 text-slate-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4" />
                </svg>
            )
        }
    };

    const message = messages[type];

    return (
        <div className="flex flex-col items-center justify-center py-16 px-6 bg-white rounded-xl border-2 border-dashed border-slate-200">
            <div className="mb-4">
                {message.icon}
            </div>
            <h3 className="text-xl font-semibold text-slate-900 mb-2">{message.title}</h3>
            <p className="text-slate-600 text-center max-w-md">{message.description}</p>
        </div>
    );
};

export default NoResults;
