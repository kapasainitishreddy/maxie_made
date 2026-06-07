/** @type {import('next').NextConfig} */
const nextConfig = { reactStrictMode: true,
  typescript: { ignoreBuildErrors: true }, async rewrites() { return [
  { source: "/api/proxy/:path*", destination: `${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8003"}/api/v1/:path*` }
]; }};
export default nextConfig;
