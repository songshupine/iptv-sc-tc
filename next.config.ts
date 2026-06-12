import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  async headers() {
    return [
      {
        // 匹配 /home/ 目录下所有的 .m3u8 文件
        source: "/home/:path*.m3u8", 
        headers: [
          {
            key: "Content-Type",
            value: "text/plain; charset=utf-8",
          },
        ],
      },
    ];
  },
};

export default nextConfig;
