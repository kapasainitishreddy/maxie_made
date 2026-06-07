"use client";
// Dev stub: when Clerk is not configured, show a friendly message instead of crashing.
export default function SignInPage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-bg">
      <div className="text-center max-w-md p-8">
        <h1 className="text-3xl font-bold mb-4">Sign in</h1>
        <p className="text-text-muted mb-6">Auth coming soon. Set NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY in .env.local to enable Clerk sign-in.</p>
        <a href="/" className="text-accent hover:underline">← Back to home</a>
      </div>
    </div>
  );
}
