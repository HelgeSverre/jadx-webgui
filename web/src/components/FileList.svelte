<script>
  import { createEventDispatcher } from "svelte";

  export let files = [];
  const dispatch = createEventDispatcher();

  function selectFile(file) {
    dispatch("selectFile", file);
  }
</script>

<div class="h-full overflow-y-auto bg-gray-200">
  {#each files as file}
    <button
      class="mb-1 block w-full cursor-pointer whitespace-nowrap rounded p-1 text-left font-mono text-xs leading-tight hover:bg-gray-300"
      on:click={() => selectFile(file)}
    >
      <span class="block opacity-50">
        {file.split("/").slice(0, -1).join("/")}
      </span>
      <span class="block pl-2">
        &rarr;
        {file.split("/").pop()}
      </span>
    </button>
  {/each}
</div>
