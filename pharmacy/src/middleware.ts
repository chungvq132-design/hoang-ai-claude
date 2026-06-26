import { withAuth } from 'next-auth/middleware'
import { NextResponse } from 'next/server'

export default withAuth(
  function middleware(req) {
    return NextResponse.next()
  },
  {
    callbacks: {
      authorized: ({ token, req }) => {
        const { pathname } = req.nextUrl
        // Store routes are public
        if (pathname.startsWith('/store') || pathname.startsWith('/api/orders')) return true
        // API product read is public (for store)
        if (pathname.startsWith('/api/products') && req.method === 'GET') return true
        // Auth routes are public
        if (pathname.startsWith('/login') || pathname.startsWith('/api/auth')) return true
        // Everything else requires auth
        return !!token
      },
    },
  }
)

export const config = {
  matcher: ['/((?!_next/static|_next/image|favicon.ico|public).*)'],
}
