<script>
  import { search } from "../store.js";

  export let endpoints = [];

  const ignored = [
    "google.com",
    "firebase.com",
    "android.com",
    "goo.gl",
    "firebaseio.com",
    "googlesource.com",
    "crashlytics.com",
    "googleadservices.com",
    "googlesyndication.com",
    "gstatic.com",
    "googleapis",
  ];

  $: uniqueEndpoints = [...new Map(endpoints.map((endpoint) => [endpoint.url, endpoint])).values()]
    .filter((endpoint) => endpoint.url?.toLowerCase().includes($search?.toLowerCase()))
    .sort((a, b) => a.url.localeCompare(b.url) || a.source.localeCompare(b.source))
    .filter((endpoint) => !ignored.some((ignore) => endpoint.url.includes(ignore)));
</script>

<div class="flex min-h-0 w-full flex-col overflow-scroll text-white p-2">
  <h2 class="mb-4 text-xl font-bold">URLs</h2>
  {#if endpoints.length === 0}
    <p>No endpoints found.</p>
  {:else}
    <div class="overflow-x-auto">
      <table class="min-w-full table-auto border-collapse">
        <thead>
          <tr class="bg-zinc-200 dark:bg-zinc-700">
            <th class="px-4 py-2 text-left">URL</th>
            <th class="px-4 py-2 text-left">Source</th>
          </tr>
        </thead>
        <tbody>
          {#each uniqueEndpoints as endpoint, i}
            <tr class={i % 2 === 0 ? "bg-zinc-100 dark:bg-zinc-800" : "bg-white dark:bg-zinc-900"}>
              <td class="border border-zinc-300 px-4 py-2 dark:border-zinc-700">{endpoint.url}</td>
              <td class="border border-zinc-300 px-4 py-2 dark:border-zinc-700">{endpoint.source}</td>
            </tr>
          {/each}
        </tbody>
      </table>
    </div>
  {/if}
</div>
