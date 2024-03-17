<script>
  import '../app.pcss';
  import { AppShell } from '@skeletonlabs/skeleton';
  import { LightSwitch } from '@skeletonlabs/skeleton';
  import { autoModeWatcher } from '@skeletonlabs/skeleton';
</script>

<svelte:head>{@html '<script>(' + autoModeWatcher.toString() + ')();</script>'}</svelte:head>

<AppShell slotSidebarLeft="bg-surface-500/5 w-56 p-4" >
  <svelte:fragment slot="sidebarLeft" >
      <nav class="list-nav">
        <ul>
          <li><a href="/">Home</a></li>
        </ul>
      </nav>
      <LightSwitch class='absolute bottom-2 left-2' />

  </svelte:fragment>
</AppShell>

<style>
</style>
