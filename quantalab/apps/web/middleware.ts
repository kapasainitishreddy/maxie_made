// Auth-bypass middleware. Uses Clerk only if key is set, otherwise no-op.
import { clerkMiddleware, createRouteMatcher } from "@clerk/nextjs/server";
import { NextResponse } from "next/server";

const clerkKey = !!process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY;
const isPublicRoute = createRouteMatcher([
  "/",
  "/sign-in(.*)",
  "/sign-up(.*)",
  "/dashboard(.*)",
  "/privacy",
  "/terms",
  "/security",
  "/api/webhook(.*)",
]);

// Real Clerk middleware - only created if key is present (avoid build errors when no key)
const realMiddleware = clerkMiddleware((auth, req) => {
  if (!isPublicRoute(req)) {
    auth().protect();
  }
});

// No-op middleware for dev (no Clerk key)
const noopMiddleware = function middleware() {
  return NextResponse.next();
};

export default clerkKey ? realMiddleware : noopMiddleware;

export const config = {
  matcher: ["/((?!_next|.*\\..*).*)", "/(api|trpc)(.*)"],
};
