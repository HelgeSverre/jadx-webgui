<script>
  export let endpoints = [];
</script>

<div class="flex min-h-0 w-full flex-col overflow-scroll text-white">
  {#if endpoints.length === 0}
    <p>No endpoints found.</p>
  {:else}
    <div class="overflow-x-auto">
      <table class="min-w-full table-auto border-collapse">
        <thead>
          <tr class="bg-gray-200 dark:bg-gray-700">
            <th class="px-4 py-2 text-left">Method</th>
            <th class="px-4 py-2 text-left">URL</th>
            <th class="px-4 py-2 text-left">Source</th>
          </tr>
        </thead>
        <tbody>
          {#each endpoints as endpoint, i}
            <tr class={i % 2 === 0 ? "bg-gray-100 dark:bg-gray-800" : "bg-white dark:bg-gray-900"}>
              <td class="border border-gray-300 px-4 py-2 dark:border-gray-700">{endpoint.method}</td>
              <td class="border border-gray-300 px-4 py-2 dark:border-gray-700">{endpoint.url}</td>
              <td class="border border-gray-300 px-4 py-2 dark:border-gray-700">{endpoint.source}</td>
            </tr>
          {/each}
        </tbody>
      </table>
    </div>
  {/if}
</div>
