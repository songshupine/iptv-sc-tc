import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  //async redirects() {
  //  return [
  //    {
        // ✅ 使用通配符 :path* 捕获 udpxy 后的所有内容（包括参数）
  //      source: "/udpxy/:path*",
        
        // ✅ 将捕获的内容原样传递到 api 路径下
  //      destination: "/api/udpxy/:path*",
        
        // ✅ 301 永久重定向，对 IPTV 播放器缓存更友好
  //      permanent: true,
  //    },
  //  ];
  //},
};

export default nextConfig;
