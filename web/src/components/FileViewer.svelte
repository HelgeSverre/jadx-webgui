<script>
  import { Clipboard } from "lucide-svelte";
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

<div class="flex min-h-0 w-full flex-col overflow-scroll bg-[#0D1116]">
  {#if $openFile && $openFile.file && $openFile.content}
    <div
      class="flex h-8 shrink-0 flex-row items-center justify-between gap-3 border-b border-zinc-700 bg-zinc-800 px-2"
    >
      <div class="w-full text-left font-mono text-xs leading-none text-yellow-300">
        {$openFile.file}
      </div>

      <button class="bg-zinc-800 text-xs text-white" on:click={() => navigator.clipboard.writeText($openFile.content)}>
        <Clipboard class="h-4 w-4" />
      </button>
    </div>

    <div class="h-full min-h-0 flex-1 overflow-auto bg-zinc-900">
      {#if $openFile.file.endsWith(".png")}
        <div class="bg-zinc-800 p-2">
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
    <div class="h-full w-full flex-1 bg-zinc-800 p-2 text-left font-mono text-xs text-zinc-400">No file selected</div>
  {/if}
</div>
