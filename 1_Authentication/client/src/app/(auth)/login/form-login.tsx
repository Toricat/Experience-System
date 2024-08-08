"use client";
import React, { useState } from 'react';
import { loginSchema } from '@/helpers/schemas/authschemas';
const LoginForm: React.FC = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [errors, setErrors] = useState<{ email?: string; password?: string }>({});

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();

        // Validate form data
        const result = loginSchema.safeParse({ email, password });

        if (!result.success) {
            // Map errors to state
            const errorMessages = result.error.errors.reduce((acc: { [key: string]: string }, curr) => {
                if (curr.path[0] === "email") {
                    acc["email"] = "Email không hợp lệ";
                }
                if (curr.path[0] === "password") {
                    acc["password"] = "Mật khẩu phải có ít nhất 6 ký tự";
                }
                return acc;
            }, {});
            setErrors(errorMessages);
            return;
        }

        setErrors({});

        console.log('Email:', email);
        console.log('Password:', password);
    };

    return (
        <form onSubmit={handleSubmit} noValidate>
            <div>
                <label htmlFor="email">Email:</label>
                <input
                    type="email"
                    id="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                />
                {errors.email && <p style={{ color: 'red', marginTop: '5px' }}>{errors.email}</p>}
            </div>
            <div>
                <label htmlFor="password">Password:</label>
                <input
                    type="password"
                    id="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                />
                {errors.password && <p style={{ color: 'red', marginTop: '5px' }}>{errors.password}</p>}
            </div>
            <button type="submit">Login</button>
        </form>
    );
};

export default LoginForm;