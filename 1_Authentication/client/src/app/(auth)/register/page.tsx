import React, { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
const RegisterPage = () => {
    const router = useRouter()

    const handleRegisterBtn = () => {

        router.push("/login")
    }
    return ( 
        <div className="">
            Register
            <button type="button" onClick={() => handleRegisterBtn()}>Register</button>
        </div>
     );
}
 
export default RegisterPage;

