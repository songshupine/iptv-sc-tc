import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  async rewrites() {
    return [
      {
        // 匹配 /udpxy/xxx, /udpxy_cmcc/xxx, /udpxy_cun/xxx 等路径
        source: "/:rule_name(udpxy|udpxy_cmcc|udpxy_cun)/:domain/:path*",
        // 转发给 Python 云函数，保持路径结构一致
        destination: "/api/udpxy/:rule_name/:domain/:path*", 
      },
    ];
  },
};

export default nextConfig;
