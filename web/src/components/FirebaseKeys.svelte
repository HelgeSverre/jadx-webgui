<script>
  import FireChecker from "./FireChecker.svelte";

  export let firebaseKeys = [];

  $: uniqueFirebaseKeys = [...new Map(firebaseKeys.map((key) => [key.key, key])).values()];
</script>

<div class="flex min-h-0 w-full flex-col overflow-scroll p-2 text-white">
  <h2 class="mb-4 text-xl font-bold">Firebase Keys</h2>
  {#if uniqueFirebaseKeys.length === 0}
    <p>No Firebase keys found.</p>
  {:else}
    <div class="list-disc pl-5">
      {#each uniqueFirebaseKeys as key}
        <div class="flex flex-row items-center justify-start gap-3">
          <FireChecker apiKey={key.key} />
          <div class="font-mono text-lg text-white">
            {key.key}
          </div>
        </div>
      {/each}
    </div>
  {/if}
</div>
