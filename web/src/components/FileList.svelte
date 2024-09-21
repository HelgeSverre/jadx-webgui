<script>
  import { createEventDispatcher } from "svelte";
  import { File, Folder, FolderOpen } from "lucide-svelte";
  import { expandedNodes, toggleNode } from "../store.js";

  export let tree;
  export let forceExpand = false;

  const dispatch = createEventDispatcher();

  // Function to handle file selection
  function selectFile(file) {
    dispatch("selectFile", file);
  }

  // Check if the node is a directory
  function isDirectory(node) {
    return node.type === "directory";
  }

  // Handle the node click for both files and directories
  function handleNodeClick(nodeName, node) {
    if (isDirectory(node)) {
      toggleNode(nodeName);
    } else {
      selectFile(node.path);
    }
  }

  $: isExpanded = (name) => forceExpand || $expandedNodes.includes(name);
</script>

<div>
  {#each Object.entries(tree) as [nodeName, node] (nodeName)}
    <button
      class="block w-full cursor-pointer whitespace-nowrap rounded p-1 text-left text-xs leading-tight hover:bg-zinc-300 focus:bg-zinc-300 focus:outline-0 dark:hover:bg-zinc-800 dark:focus:bg-zinc-800"
      on:click={() => handleNodeClick(nodeName, node)}
    >
      <span class="flex flex-row items-center justify-start gap-2">
        {#if isDirectory(node)}
          <span class="inline-block text-zinc-900 dark:text-zinc-100">
            {#if isExpanded(nodeName)}
              <FolderOpen size="14" class="inline-block fill-zinc-800 stroke-zinc-400 stroke-2" />
            {:else}
              <Folder size="14" class="inline-block fill-zinc-800 stroke-zinc-400 stroke-2" />
            {/if}
          </span>
        {:else}
          <span class="inline-block text-zinc-900 dark:text-zinc-100">
            <File size="14" class="inline-block" />
          </span>
        {/if}
        <span class="inline-block text-zinc-900 dark:text-zinc-300">{nodeName}</span>
      </span>
    </button>
    {#if isDirectory(node) && isExpanded(nodeName)}
      <div class="ml-3 w-full">
        <svelte:self tree={node.children} forceExpand={forceExpand} on:selectFile />
      </div>
    {/if}
  {/each}
</div>
