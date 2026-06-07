// Auth-bypass middleware. Always exports a function, uses Clerk only if key set.
import { clerkMiddleware, createRouteMatcher } from "@clerk/nextjs/server";
import { NextResponse } from "next/server";

const clerkKey = !!process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY;
const isPublic = createRouteMatcher(["/", "/sign-in(.*)", "/sign-up(.*)", "/(dashboard)(.*)"]);

const realClerkMiddleware = clerkMiddleware((a, r) => {
  if (!isPublic(r)) a().protect();
});

export default clerkKey
  ? realClerkMiddleware
  : function middleware() {
      return NextResponse.next();
    };

export const config = { matcher: ["/((?!_next|.*\\..*).*)", "/(api|trpc)(.*)"] };
