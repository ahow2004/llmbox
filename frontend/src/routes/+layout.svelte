<!-- src/routes/+layout.svelte -->
<script>
	import { ClerkProvider, ClerkLoaded, SignedIn, SignedOut, UserButton } from '@clerk/clerk-js';
	import { PUBLIC_CLERK_PUBLISHABLE_KEY } from '$env/static/public';
</script>

<ClerkProvider publishableKey={PUBLIC_CLERK_PUBLISHABLE_KEY}>
	<ClerkLoaded>
		<header style="display: flex; justify-content: space-between; align-items: center;">
			<h1>🧠 LLMBox</h1>
			<SignedIn>
				<UserButton />
			</SignedIn>
			<SignedOut>
				<a href="https://clerk.com/sign-in">Sign In</a>
			</SignedOut>
		</header>

		<slot />
	</ClerkLoaded>
</ClerkProvider>


<slot /> 
