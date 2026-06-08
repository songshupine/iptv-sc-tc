import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // 强制关闭尾部斜杠，防止产生多余的 308 重定向
  trailingSlash: false, 
  
  async redirects() {
    return [
      {
        // 1. 匹配规则：
        // 使用正则表达式 /(udpxy.*)/:path* 
        // (udpxy.*) 会捕获 udpxy, udpxy_cmcc, udpxy_cun 等作为第一个参数 ($1)
        // :path* 会捕获后面的所有内容（如 192.168.2.1:4022/hls）作为第二个参数 ($2)
        source: "/(udpxy.*)/:path*",
        
        // 2. 重定向目标：
        // /api/$2 将 IP 和端口路径透传给 API
        // ?udpxy_type=$1 将捕获到的 udpxy 类型作为查询参数传递
        destination: "/api/$2?udpxy_type=$1",
        
        // 301 永久重定向，对浏览器和客户端缓存更友好
        permanent: true,
      },
    ];
  },
};

export default nextConfig;
