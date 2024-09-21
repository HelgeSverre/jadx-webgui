<script>
  import { Clipboard, Text, WrapText } from "lucide-svelte";
  import { HighlightAuto, LineNumbers } from "svelte-highlight";
  import { openFile } from "../store.js";
  import { githubDark } from "svelte-highlight/styles";

  // Function to convert raw bytes to a Blob URL
  function bytesToImageUrl(bytes) {
    if (bytes) {
      const blob = new Blob([new Uint8Array(bytes)], { type: "image/png" });
      return URL.createObjectURL(blob);
    }

    return null;
  }
</script>

<svelte:head>
  {@html githubDark}
</svelte:head>

<div class="flex h-full w-full flex-1 flex-col overflow-hidden">
  {#if $openFile && $openFile.file && $openFile.content}
    <div
      class="flex h-8 shrink-0 flex-row items-center justify-between gap-3 border-b border-gray-700 bg-gray-800 px-2"
    >
      <div class="w-full text-left font-mono text-xs leading-none text-yellow-300">
        {$openFile.file}
      </div>

      <button class="bg-gray-800 text-xs text-white" on:click={() => navigator.clipboard.writeText($openFile.content)}>
        <Clipboard class="h-4 w-4" />
      </button>
    </div>

    <div class="overflow-scroll bg-gray-900">
      {#if $openFile.file.endsWith(".png")}
        <div class="bg-gray-800 p-2">
          {bytesToImageUrl($openFile.content)}
          <img src={bytesToImageUrl($openFile.content)} alt={$openFile.file} />
        </div>
      {:else}
        <HighlightAuto code={$openFile.content} let:highlighted>
          <LineNumbers highlighted={highlighted} />
        </HighlightAuto>
      {/if}
    </div>
  {:else}
    <div class="w-full bg-gray-800 p-2 text-left font-mono text-xs text-gray-400">No file selected</div>
  {/if}
</div>
