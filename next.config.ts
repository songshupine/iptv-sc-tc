import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  async rewrites() {
    return [
      {
        source: "/udpxy/:path*",       // ✅ 必须包含斜杠
        destination: "/api/udpxy/:path*",
      },
    ];
  },
};

export default nextConfig;
