import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  const url = request.nextUrl.clone();
  
  // 拦截 /udpxy/ 开头的请求
  if (url.pathname.startsWith('/udpxy/')) {
    // 1. 将路径中的冒号 : 替换为双下划线 __ (兼容带端口的情况)
    const newPath = url.pathname.replace(/:/g, '__');
    url.pathname = newPath;
    
    // 2. 将请求转发到 /api/udpxy/ 下
    url.pathname = url.pathname.replace('/udpxy/', '/api/udpxy/');
    
    return NextResponse.rewrite(url);
  }
  
  return NextResponse.next();
}

// 【核心修复】使用正则表达式数组，确保能匹配多级路径
export const config = {
  matcher: ['/udpxy/:path*', '/udpxy'], 
};

