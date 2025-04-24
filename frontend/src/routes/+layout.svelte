<script>
  import { ClerkProvider } from '@clerk/clerk-js';
  import { browser } from '$app/environment';

  const publishableKey = import.meta.env.PUBLIC_CLERK_PUBLISHABLE_KEY;
</script>

{#if browser}
  <ClerkProvider publishableKey={publishableKey}>
    <slot />
  </ClerkProvider>
{:else}
  <slot />
{/if}
