<script>
  import { afterUpdate, onMount } from "svelte";
  import classNames from "classnames";
  import { clearLogs, logs } from "../store.js";
  import { formatTimestamp } from "../utils.js";
  import { ChevronDown } from "lucide-svelte";

  const maxLogs = 100;

  let console;
  let shouldScroll = true;

  let collapsed = false;

  onMount(() => {
    scrollToBottom();
  });

  afterUpdate(() => {
    if (shouldScroll) {
      scrollToBottom();
    }
  });

  function scrollToBottom() {
    if (console) {
      console.scrollTop = console.scrollHeight;
    }
  }

  function handleScroll() {
    const { scrollTop, scrollHeight, clientHeight } = console;
    shouldScroll = scrollTop + clientHeight >= scrollHeight - 5;
  }

  $: latestLogItems = $logs.slice(-maxLogs);
</script>

<footer class="bg-gray-800 dark:bg-black">
  <div class="flex w-full items-center justify-between gap-2 bg-gray-900 px-2 py-1 leading-10 dark:bg-gray-950">
    <h1 class="inline-block font-mono text-xs font-medium text-white">
      <span>Console</span>
      <span class="text-[10px] text-gray-400 dark:text-gray-500">({$logs.length.toLocaleString()})</span>
    </h1>

    <div class="flex items-center justify-end gap-2">
      <button
        class="inline-block cursor-pointer rounded text-xs font-semibold text-gray-200/50 hover:text-gray-200 focus:outline-none focus:ring-2 focus:ring-white focus:ring-opacity-50"
        on:click={() => clearLogs()}
      >
        Clear
      </button>
      <button
        class="inline-block cursor-pointer overflow-hidden rounded text-xs font-semibold text-gray-200/50 hover:text-gray-200 focus:outline-none focus:ring-2 focus:ring-white focus:ring-opacity-50"
        on:click={() => (collapsed = !collapsed)}
      >
        <ChevronDown
          class={classNames("size-4 duration-200 ease-in-out", {
            "rotate-180 transform": collapsed,
          })}
        />
      </button>
    </div>
  </div>

  <div
    bind:this={console}
    on:scroll={handleScroll}
    class={classNames("w-full font-mono text-sm text-white duration-200 ease-in-out", {
      "max-h-0 overflow-hidden ": collapsed,
      "max-h-64 min-h-32 overflow-x-hidden overflow-y-scroll text-wrap break-words ": !collapsed,
    })}
  >
    {#each latestLogItems as log}
      <div
        class={classNames(
          "group flex flex-row items-start  gap-2 px-2 text-xs font-normal leading-normal hover:!bg-white/20",
          {
            "font-bold text-red-500": log.type === "error",
            "bg-green-950 text-green-400 dark:bg-opacity-20": log.type === "success",
            "text-yellow-500": log.type === "warn",
            "text-gray-400": log.type === "comment",
            "text-purple-400": log.type === "debug",
            "text-sky-400": log.type === "info",
          },
        )}
      >
        <div class="block whitespace-nowrap tabular-nums tracking-tight text-gray-400">
          {formatTimestamp(log.timestamp)}:
        </div>
        <div class="inline-block">{log.message}</div>
      </div>
    {/each}
  </div>
</footer>
