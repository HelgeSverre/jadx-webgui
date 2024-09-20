<script>
  import { Clipboard, Text, WrapText } from "lucide-svelte";

  export let content = "";
  export let file = "";

  let softwrap = false;

  // Function to convert raw bytes to a Blob URL
  function bytesToImageUrl(bytes) {
    if (bytes) {
      const blob = new Blob([new Uint8Array(bytes)], { type: "image/png" });
      return URL.createObjectURL(blob);
    }

    return null;
  }
</script>

<div class="flex h-full w-full flex-1 flex-col overflow-hidden">
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
          {bytesToImageUrl(content)}
          <img src={bytesToImageUrl(content)} alt={file} />
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
