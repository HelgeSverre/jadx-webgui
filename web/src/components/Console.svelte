<script>
  import { afterUpdate, onMount } from "svelte";
  import classNames from "classnames";
  import { clearLogs, logs, settings } from "../store.js";
  import { formatTimestamp } from "../utils.js";
  import { ChevronDown, ChevronRight } from "lucide-svelte";

  let console;
  let shouldScroll = true;

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

  function groupDebugLogs(logs) {
    let groupedLogs = [];
    let currentDebugGroup = null;

    for (let log of logs) {
      if (log.type === "debug") {
        if (!currentDebugGroup) {
          currentDebugGroup = { type: "debug-group", items: [log], collapsed: true };
          groupedLogs.push(currentDebugGroup);
        } else {
          currentDebugGroup.items.push(log);
        }
      } else {
        currentDebugGroup = null;
        groupedLogs.push(log);
      }
    }

    return groupedLogs;
  }

  $: latestLogItems = $settings.groupConsoleItems
    ? groupDebugLogs($logs.slice(-$settings.consoleMaxItems))
    : $logs.slice(-$settings.consoleMaxItems);
</script>

<footer class="bg-zinc-800 dark:bg-black">
  <div
    class="flex h-8 w-full items-center justify-between gap-2 border-b border-zinc-800/50 bg-zinc-900 p-2 dark:bg-zinc-950"
  >
    <h1 class="block font-mono text-xs font-medium leading-loose text-white">
      <span>Console</span>
      <span class="text-[10px] text-zinc-400 dark:text-zinc-500">({$logs.length.toLocaleString()})</span>
    </h1>
    <div class="flex items-center justify-end gap-2">
      <button
        class="inline-block cursor-pointer rounded-sm text-xs font-semibold text-zinc-200/50 hover:text-zinc-200 focus:outline-none focus:ring-2 focus:ring-white focus:ring-opacity-50"
        on:click={() => ($settings.groupConsoleItems = !$settings.groupConsoleItems)}
      >
        Group
      </button>
      <button
        class="inline-block cursor-pointer rounded-sm text-xs font-semibold text-zinc-200/50 hover:text-zinc-200 focus:outline-none focus:ring-2 focus:ring-white focus:ring-opacity-50"
        on:click={() => clearLogs()}
      >
        Clear
      </button>
      <button
        class="inline-block cursor-pointer overflow-hidden rounded-sm text-xs font-semibold text-zinc-200/50 hover:text-zinc-200 focus:outline-none focus:ring-2 focus:ring-white focus:ring-opacity-50"
        on:click={() => ($settings.consoleCollapsed = !$settings.consoleCollapsed)}
      >
        <ChevronDown
          class={classNames("size-4 duration-200 ease-in-out", {
            "rotate-180 transform": $settings.consoleCollapsed,
          })}
        />
      </button>
    </div>
  </div>
  <div
    bind:this={console}
    on:scroll={handleScroll}
    class={classNames("w-full font-mono text-sm text-white duration-200 ease-in-out", {
      "max-h-0 overflow-hidden": $settings.consoleCollapsed,
      "max-h-64 min-h-32 overflow-x-hidden overflow-y-scroll text-wrap break-words py-2": !$settings.consoleCollapsed,
    })}
  >
    {#each latestLogItems as log}
      {#if $settings.groupConsoleItems && log.type === "debug-group" && log.items.length > 1}
        <div class="group flex flex-col">
          <button
            on:click={() => (log.collapsed = !log.collapsed)}
            class="flex cursor-pointer items-center gap-1 px-2 text-left text-xs font-normal text-purple-400 hover:!bg-white/20"
          >
            <span class="block whitespace-nowrap tabular-nums tracking-tight text-zinc-400">
              {formatTimestamp(log.items[0].timestamp)}:
            </span>

            <span class="inline-block">{log.items.length} debug messages</span>
            {#if log.collapsed}
              <ChevronRight class="size-3" />
            {:else}
              <ChevronDown class="size-3" />
            {/if}
          </button>
          {#if !log.collapsed}
            {#each log.items as debugItem}
              <div class="ml-4 flex flex-row items-start gap-2 px-2 text-xs font-normal leading-normal text-purple-400">
                <div class="block whitespace-nowrap tabular-nums tracking-tight text-zinc-400">
                  {formatTimestamp(debugItem.timestamp)}:
                </div>
                <div class="inline-block">{debugItem.message}</div>
              </div>
            {/each}
          {/if}
        </div>
      {:else}
        <div
          class={classNames(
            "group flex flex-row items-start gap-2 px-2 text-xs font-normal leading-normal hover:!bg-white/20",
            {
              "font-bold text-red-500": log.type === "error",
              "bg-green-950 text-green-400 dark:bg-opacity-20": log.type === "success",
              "text-yellow-500": log.type === "warn",
              "text-zinc-400": log.type === "comment",
              "text-purple-400": log.type === "debug",
              "text-sky-400": log.type === "info",
              "text-yellow-300": log.type === "notice",
            },
          )}
        >
          <div class="block whitespace-nowrap tabular-nums tracking-tight text-zinc-400">
            {formatTimestamp(log.timestamp)}:
          </div>
          <div class="inline-block">{log.message}</div>
        </div>
      {/if}
    {/each}
  </div>
</footer>
