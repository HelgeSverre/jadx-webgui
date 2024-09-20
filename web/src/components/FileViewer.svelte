<script>
  import { Clipboard, Text, WrapText } from "lucide-svelte";

  export let content = "";
  export let file = "";

  let softwrap = false;
</script>

<div class="flex h-full flex-col overflow-hidden rounded">
  {#if file}
    <div
      class="flex h-8 shrink-0 flex-row items-center justify-between gap-3 border-b border-gray-700 bg-gray-800 px-2"
    >
      <div class="w-full text-left font-mono text-xs leading-none text-yellow-300">
        {file.split("/").pop()}
      </div>

      <button
        class="flex items-center justify-center whitespace-nowrap bg-gray-800 text-xs text-white"
        on:click={() => (softwrap = !softwrap)}
      >
        {#if softwrap}
          <Text class="h-4 w-4" />
        {:else}
          <WrapText class="h-4 w-4" />
        {/if}
      </button>

      <button class="bg-gray-800 text-xs text-white" on:click={() => navigator.clipboard.writeText(content)}>
        <Clipboard class="h-4 w-4" />
      </button>
    </div>

    <div class="overflow-scroll bg-gray-900">
      {#if file.endsWith(".png")}
        <div class="bg-gray-800 p-2">
          <img src="data:image/png;base64,{content}" alt="Image preview" />
        </div>
      {:else if file.endsWith(".json")}
        <pre
          class="p-2 text-xs text-white"
          class:whitespace-pre-wrap={!softwrap}
          class:whitespace-pre={!softwrap}>{JSON.stringify(JSON.parse(content), null, 2)}</pre>
      {:else}
        <pre
          class="p-2 text-xs text-white"
          class:whitespace-pre-wrap={!softwrap}
          class:whitespace-pre={!softwrap}>{content}</pre>
      {/if}
    </div>
  {:else}
    <div class="w-full bg-gray-800 p-2 text-left font-mono text-xs text-gray-400">No file selected</div>
  {/if}
</div>
