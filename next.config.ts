const nextConfig: NextConfig = {
  trailingSlash: false,
  async rewrites() {
    return [
      {
        // 匹配 /udpxy, /udpxy_cmcc 等路径
        source: "/:rule_name(udpxy|udpxy_cmcc|udpxy_cun)",
        // 转发给云函数根路径，不再在路径中传递 domain
        destination: "/api/udpxy", 
      },
    ];
  },
};
