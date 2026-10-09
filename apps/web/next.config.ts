import type { NextConfig } from "next";

// The browser calls /api/v1/* on the web app's own origin; Next forwards it to the API.
// This keeps the API URL out of client code and avoids CORS in the browser.
const apiUrl = process.env.SAILPREP_API_URL ?? "http://localhost:8000";

const nextConfig: NextConfig = {
  output: "standalone",
  // react-pdf renders on the server; keep it out of the bundler.
  serverExternalPackages: ["@react-pdf/renderer"],
  async rewrites() {
    return [{ source: "/api/v1/:path*", destination: `${apiUrl}/api/v1/:path*` }];
  },
};

export default nextConfig;
