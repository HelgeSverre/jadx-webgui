<script>
  export let firebaseKeys = [];

  $: uniqueFirebaseKeys = [...new Map(firebaseKeys.map((key) => [key.key, key])).values()];
</script>

<div class="bg-white p-4 text-zinc-900 dark:bg-zinc-900 dark:text-zinc-100">
  <h2 class="mb-4 text-xl font-bold">Firebase Keys</h2>
  {#if uniqueFirebaseKeys.length === 0}
    <p>No Firebase keys found.</p>
  {:else}
    <ul class="list-disc pl-5">
      {#each uniqueFirebaseKeys as key}
        <li>{key.key}</li>
      {/each}
    </ul>
  {/if}
</div>
