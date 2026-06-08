import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  async rewrites() {
    return [
      {
        // 匹配前端访问的路径，例如：/udpxy/192.168.2.30:8888
        source: "/:rule_name(udpxy|udpxy_cmcc|udpxy_cun)/:domain/:path*",
        
        // 【核心修改】去掉 destination 中的 :rule_name
        // 这样转发给云函数的路径就变成了：/api/udpxy/192.168.2.30:8888
        destination: "/api/udpxy/:domain/:path*", 
      },
    ];
  },
};

export default nextConfig;
