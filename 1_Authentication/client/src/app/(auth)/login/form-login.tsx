"use client";
import React, { useState } from 'react';
import { loginSchema } from '@/helpers/schemas/authschemas';

const LoginForm: React.FC = () => {
    const [email, setEmail] = useState<string>('');
    const [password, setPassword] = useState<string>('');
    const [errors, setErrors] = useState<{ email?: string; password?: string }>({});

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();

        const result = loginSchema.safeParse({ email, password });

        if (!result.success) {
            const errorMessages = result.error.errors.reduce(
                (acc, { path, message }) => ({ ...acc, [path[0]]: message }),{}
            );
            setErrors(errorMessages);
        } else {
            setErrors({});
            console.log('Email:', email);
            console.log('Password:', password);
        }
    };

    const handleGoogleLogin = () => {
        // Thêm logic đăng nhập với Google ở đây
        console.log("Đăng nhập bằng Google");
    };

    return (
        <form onSubmit={handleSubmit} noValidate className="text-left bg-white p-6 rounded-lg shadow-md max-w-md mx-auto">
            <div className="mb-4">
                <label htmlFor="email" className="text-gray-700 font-semibold">Email:</label>
                <input
                    type="email"
                    id="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    className="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
                {errors.email && <p className='text-red-500 text-sm mt-1'>{errors.email}</p>}
            </div>
            <div className="mb-4">
                <label htmlFor="password" className="text-gray-700 font-semibold">Password:</label>
                <input
                    type="password"
                    id="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    className="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
                {errors.password && <p className='text-red-500 text-sm mt-1'>{errors.password}</p>}
            </div>
            <div className="flex justify-between items-center mb-4">
                <button
                    type="submit"
                    className="w-full bg-blue-500 text-white py-2 rounded-md hover:bg-blue-600 transition duration-200">
                    Login
                </button>
            </div>
            <div className="flex justify-center items-center mb-4">
                <button
                    type="button"
                    onClick={handleGoogleLogin}
                    className="w-full bg-red-500 text-white py-2 rounded-md hover:bg-red-600 transition duration-200">
                    Đăng nhập bằng Google
                </button>
            </div>
            <div className="text-center">
                <a href="/forgot-password" className="text-blue-500 hover:underline">Forgot Password?</a>
            </div>
            <div className="text-center mt-4">
                <span className="text-gray-600">Chưa có tài khoản?</span>
                <a href="/register" className="text-blue-500 hover:underline ml-1">Đăng ký</a>
            </div>
        </form>
    );
};

export default LoginForm;
