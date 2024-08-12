// src/lib/token.ts
import Cookies from 'js-cookie';
import {jwtDecode} from "jwt-decode";
import { AUTH_TOKEN_KEY, TokenState } from '@/constants';

interface JwtPayload {
  exp: number;
}

const setTokenExpiration = (expiration: number): void => {
  TokenState.expiration = expiration;
};

const updateTokenExpiration = (token: string): void => {
  try {
    const { exp } = jwtDecode<JwtPayload>(token);
    setTokenExpiration(exp * 1000); 
  } catch (error) {
    console.error('Error decoding token:', error);
    setTokenExpiration(0);
  }
};

export const getAuthToken = (): string | null => {
  const token = Cookies.get(AUTH_TOKEN_KEY) || null;
  if (token && TokenState.expiration === null) {
    updateTokenExpiration(token);
  }
  return token;
};

export const setAuthToken = (token: string): void => {
  Cookies.set(AUTH_TOKEN_KEY, token, { expires: 7, secure: true, sameSite: 'Strict' });
  updateTokenExpiration(token);
};

export const removeAuthToken = (): void => {
  Cookies.remove(AUTH_TOKEN_KEY);
  setTokenExpiration(0);
};

export const handleTokenExpiration = (): string | undefined => {
  const token = getAuthToken();
  if (!token || (TokenState.expiration !== null && Date.now() >= TokenState.expiration)) {
    removeAuthToken();
    sessionStorage.clear();
    window.location.href = '/signin';
    throw new Error('Token expired');
  }

  return token;
};
