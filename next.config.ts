import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  trailingSlash: false,
  // 不要写 rewrites，让 Middleware 全权处理
};

export default nextConfig;
