async rewrites() {
  return [
    {
      source: "/udpxy/:path*",
      destination: "/api/udpxy/:path*",
    },
  ];
},
