import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  trailingSlash: false, 
  async redirects() {
    return [
      {
        source: "/udpxy/:path*",
        destination: "/api/udpxy/:path*",
        // 使用 301 永久重定向，对 SEO 和缓存更友好；若需临时测试可改为 302
        permanent: true, 
      },
    ];
  },
};

export default nextConfig;
