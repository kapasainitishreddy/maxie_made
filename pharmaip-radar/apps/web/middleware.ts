// Auth-bypass middleware. Always exports a function, but uses Clerk only if key is set.
import { clerkMiddleware, createRouteMatcher } from "@clerk/nextjs/server";
import { NextResponse } from "next/server";

const clerkKey = !!process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY;
const isPublicRoute = createRouteMatcher([
  "/",
  "/pricing",
  "/sign-in(.*)",
  "/sign-up(.*)",
  "/api/webhooks(.*)",
  "/(dashboard)(.*)",
]);

// In dev (no Clerk key), just pass through. In prod, use Clerk.
const realClerkMiddleware = clerkMiddleware((auth, req) => {
  if (!isPublicRoute(req)) auth().protect();
});

export default clerkKey
  ? realClerkMiddleware
  : function middleware() {
      return NextResponse.next();
    };

export const config = {
  matcher: [
    "/((?!_next|[^?]*\\.(?:html?|css|js(?!on)|jpe?g|webp|png|gif|svg|ttf|woff2?|ico|csv|docx?|xlsx?|zip|webmanifest)).*)",
    "/(api|trpc)(.*)",
  ],
};
