import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "FastAPI + EdgeOne Pages",
  description: "Deploy high-performance FastAPI applications as serverless functions on EdgeOne Pages. With automatic OpenAPI docs, Pydantic validation, and async support.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en-US">
      <head>
        <link rel="icon" href="/fastapi-favicon.svg" />
      </head>
      <body className="antialiased">
        {children}
      </body>
    </html>
  );
}
