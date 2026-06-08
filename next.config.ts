import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  trailingSlash: false,
  async rewrites() {
    return [
      {
        source: "/udpxy/:path*",
        // 【核心】将路径中的冒号替换为双下划线，绕过网关拦截
        destination: "/api/udpxy/:path*", 
      },
    ];
  },
};

export default nextConfig;
