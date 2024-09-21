<script>
  export let firebaseKeys = [];
</script>

<div class="bg-white p-4 text-gray-900 dark:bg-gray-900 dark:text-gray-100">
  <h2 class="mb-4 text-xl font-bold">Firebase Keys</h2>
  {#if firebaseKeys.length === 0}
    <p>No Firebase keys found.</p>
  {:else}
    <ul class="list-disc pl-5">
      {#each firebaseKeys as key}
        <li>{key.key}</li>
      {/each}
    </ul>
  {/if}
</div>
