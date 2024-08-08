import Cookies from 'js-cookie';
import { jwtDecode } from "jwt-decode";
import { AUTH_TOKEN_KEY } from '@/constants';

interface JwtPayload {
  exp: number;
}
export const getAuthToken = (): string | null => {
  return Cookies.get(AUTH_TOKEN_KEY ) || null;
};

export const setAuthToken = (token: string): void => {
  Cookies.set(AUTH_TOKEN_KEY , token, { expires: 7, secure: true, sameSite: 'Strict' });
};

export const removeAuthToken = (): void => {
  Cookies.remove(AUTH_TOKEN_KEY );
};

export const isTokenExpired = (token: string): boolean => {
  try {
    const decodedToken = jwtDecode<JwtPayload>(token);
    const expiry = decodedToken.exp;
    const now = Math.floor(Date.now() / 1000);
    return now > expiry;
  } catch (error) {
    console.error('Error decoding token:', error);
    return true; 
  }
};

export const handleTokenExpiration = (): string | undefined => {
  const token = getAuthToken();
  if (!token) {
    sessionStorage.clear();
    return undefined;
  }
  if (token && isTokenExpired(token)) {
    removeAuthToken();
    sessionStorage.clear();
    window.location.href = '/signin';
    throw new Error('Token expired');
  }
  return token;
};