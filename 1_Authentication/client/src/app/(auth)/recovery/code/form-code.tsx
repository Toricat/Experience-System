"use client";
import React, { useState } from 'react';
import { CodeSchema } from '@/helpers/schemas/authschemas';
import { useRouter } from 'next/navigation';
import Link from 'next/link'
const CodeForm: React.FC = () => {
    const [code, setCode] = useState<string>('');
    const [errors, setErrors] = useState<{ code?: string; }>({});
    const router = useRouter();

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();

        const result = CodeSchema.safeParse({ code });

        if (!result.success) {
            const errorMessages = result.error.errors.reduce(
                (acc, { path, message }) => ({ ...acc, [path[0]]: message }),{}
            );
            setErrors(errorMessages);
        } else {
            setErrors({});
            router.push('/recovery/code/reset');
        }


    };


    return (
        <form onSubmit={handleSubmit} noValidate className="text-left bg-white p-6 rounded-lg shadow-md  mx-auto">
            <div className="mb-4">
                <label htmlFor="code" className="text-gray-700 font-semibold">Code:</label>
                <input
                    type="code"
                    id="code"
                    value={code}
                    placeholder='Enter your code'
                    onChange={(e) => setCode(e.target.value)}
                    className="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
                {errors.code && <p className='text-red-500 text-sm mt-1'>{errors.code}</p>}
            </div>
 
            <div className="flex justify-between items-center mb-2">
                <button
                    type="submit"
                    className="w-full bg-blue-500 text-white py-2 rounded-md hover:bg-blue-600 transition duration-200">
                    Continue
                </button>
            </div>
      
            
        </form>
    );
};

export default CodeForm;
