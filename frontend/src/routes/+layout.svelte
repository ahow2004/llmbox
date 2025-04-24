<script>
  import { browser } from '$app/environment';
</script>

{#if browser}
  <slot />
{:else}
  <!-- SSR fallback -->
  <slot />
{/if}
