import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;
  const sessionToken = request.cookies.get('auth-token');

  if (
    pathname.startsWith('/_next') ||
    pathname.startsWith('/api') ||
    pathname.includes('/static') ||
    pathname.includes('.') ||
    pathname.endsWith('.ico')  
    // || pathname ===('/')
  ) {
    return NextResponse.next();
  }

  if (pathname ==="/" ) {
    return NextResponse.redirect(new URL('/login', request.url));
  }
  
  if (sessionToken && (pathname.startsWith('/login') || pathname.startsWith('/register'))) {
    const response = NextResponse.redirect(new URL('/dashboard', request.url));
    return response;
  }


  if (!sessionToken && (pathname.startsWith('/login') || pathname.startsWith('/register'))) {
    return NextResponse.next();
  }

  if (!sessionToken) {
    const response = NextResponse.redirect(new URL('/login', request.url));
    return response;
  }

  const response = NextResponse.next();
  
  return response;
}

export const config = {
  matcher: [
    '/((?!_next/static|_next/image|api|favicon\\.ico|.*\\..*).*)'
  ],
};
