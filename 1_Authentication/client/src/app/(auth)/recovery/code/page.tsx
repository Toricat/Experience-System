import React from 'react';
import CodeForm from '@/app/(auth)/recovery/code/form-code';

const CodePage = () => {
    return (
        <div className="h-full w-full flex items-center justify-center bg-gray-100">
            <div className="h-full w-full flex flex-col items-center justify-center">
                <h1 className="text-3xl font-bold text-center text-gray-800 mb-4">Input Code</h1>
                <CodeForm/>
            </div>
        </div>
    );
};

export default CodePage;