<script>
  import ListItemPlaceholder from './ListItemPlaceholder.svelte';

  const randomItemQuantity = (Math.random() * 5) + 1;
</script>

<ul>
  {#each { length: randomItemQuantity } as _}
    <ListItemPlaceholder />
  {/each}
</ul>
