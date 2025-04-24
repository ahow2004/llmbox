<script lang="ts">
  import { ClerkProvider } from 'clerk-sveltekit/client';
  import { PUBLIC_CLERK_PUBLISHABLE_KEY } from '$env/static/public';
</script>

<ClerkProvider publishableKey={PUBLIC_CLERK_PUBLISHABLE_KEY}>
  <slot />
</ClerkProvider>
