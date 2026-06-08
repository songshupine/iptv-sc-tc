import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  const url = request.nextUrl.clone();
  // 如果路径包含 /udpxy/，将后续的冒号替换为 __
  if (url.pathname.startsWith('/udpxy/')) {
    const prefix = '/udpxy/';
    const rest = url.pathname.slice(prefix.length);
    // 将 IP 中的 : 替换为 __
    url.pathname = prefix + rest.replace(/:/g, '__');
  }
  return NextResponse.rewrite(url);
}

export const config = {
  matcher: '/udpxy/:path*',
};
