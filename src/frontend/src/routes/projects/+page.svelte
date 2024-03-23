<script>
  import PlusSignIcon from '../../components/assets/PlusSignIcon.svelte';

  let projects = [{ id: '', name: '', description: '' }];
</script>

<div class="container mx-auto p-8 space-y-8">
  <h1 class="h1">Projects</h1>

  <nav class="list-nav">
    <ul>
      {#each projects as { id, name, description }}
        <li>
          <a href={`/projects/${id}`}>
            <span class="flex-auto">{name}</span>
            <span class="flex-auto project-description text-xs"
              >{description}</span
            >
          </a>
        </li>
      {/each}
    </ul>
    <button type="button" class="btn variant-soft-surface flex-auto mx-auto">
      <PlusSignIcon />
    </button>
  </nav>
</div>
