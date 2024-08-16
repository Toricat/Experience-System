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
    || pathname ===('/')
  ) {
    return NextResponse.next();
  }


  
  if (sessionToken && (pathname.startsWith('/login') || pathname.startsWith('/register') || pathname.startsWith('/recovery') || pathname.startsWith('/verify'))) {
    const response = NextResponse.redirect(new URL('/dashboard', request.url));
    return response;
  }


  if (!sessionToken && (pathname.startsWith('/login') || pathname.startsWith('/register') || pathname.startsWith('/recovery') || pathname.startsWith('/verify'))) {
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
