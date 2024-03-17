<script>
  import '../app.pcss';
  import { AppShell } from '@skeletonlabs/skeleton';
  import { LightSwitch } from '@skeletonlabs/skeleton';
  import { autoModeWatcher } from '@skeletonlabs/skeleton';
</script>

<AppShell slotSidebarLeft="bg-surface-500/5 w-0 lg:w-64 p-4">
  <svelte:fragment slot="sidebarLeft">
    <!-- User Profile -->
    <a class="user-profile-img-link flex flex-row items-center" href="/">
      <div class="placeholder-test w-10 my-2 placeholder-circle"></div>
      <div class="user-name mx-5">
        <span class='span'>username</span>
      </div>
    </a>
    <hr>
    <nav class="list-nav">
      <ul>
        <li><a href="/">Home</a></li>
      </ul>
    </nav>
    <LightSwitch class="absolute bottom-2 left-2 hidden lg:block" />
  </svelte:fragment>
  <slot />
</AppShell>

<style>
</style>
