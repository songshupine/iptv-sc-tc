import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  async rewrites() {
    return [
      {
        source: "/udpxy",       // ✅ 必须包含斜杠
        destination: "/api/udpxy",
      },
    ];
  },
};

export default nextConfig;
