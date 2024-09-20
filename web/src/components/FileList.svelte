<script>
  import { createEventDispatcher } from "svelte";
  import { Minus, Plus } from "lucide-svelte";
  import { addLog } from "../store.js";

  export let tree;
  export let forceExpand = false;

  const dispatch = createEventDispatcher();

  // Track expanded nodes in the local state
  let expandedNodes = new Set();

  // Toggle a node's expansion state
  function toggleNode(name) {
    if (isExpanded(name)) {
      expandedNodes.delete(name);
    } else {
      expandedNodes.add(name);
    }

    expandedNodes = expandedNodes;
  }

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

  $: isExpanded = (name) => forceExpand || expandedNodes.has(name);
</script>

<div class="overflow-auto bg-gray-200 dark:bg-gray-950">
  {#each Object.entries(tree) as [nodeName, node] (nodeName)}
    <div>
      <button
        class="mb-1 block w-full cursor-pointer whitespace-nowrap rounded p-1 text-left font-mono text-xs leading-tight hover:bg-gray-300 dark:hover:bg-gray-800"
        on:click={() => handleNodeClick(nodeName, node)}
      >
        <div class="flex flex-row items-center justify-start gap-1">
          {#if isDirectory(node)}
            <span class="inline-block text-gray-900 dark:text-gray-100">
              {#if isExpanded(nodeName)}
                <Minus size="14" class="inline-block" />
              {:else}
                <Plus size="14" class="inline-block" />
              {/if}
            </span>
          {/if}
          <span class="inline-block text-gray-900 dark:text-gray-100">{nodeName}</span>
        </div>
      </button>
      {#if isDirectory(node) && isExpanded(nodeName)}
        <div class="pl-4">
          <svelte:self tree={node.children} forceExpand={forceExpand} on:selectFile />
        </div>
      {/if}
    </div>
  {/each}
</div>
