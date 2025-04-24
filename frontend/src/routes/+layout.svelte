<!-- src/routes/+layout.svelte -->
<script>
  import { ClerkProvider } from '@clerk/clerk-js';
</script>

<ClerkProvider publishableKey={import.meta.env.VITE_CLERK_PUBLISHABLE_KEY}>
  <slot />
</ClerkProvider>
