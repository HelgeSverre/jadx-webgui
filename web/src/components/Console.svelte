<script>
  import { afterUpdate, onMount } from "svelte";
  import classNames from "classnames";

  export let logs = [];
  let element;
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
    if (element) {
      element.scrollTop = element.scrollHeight;
    }
  }

  function handleScroll() {
    const { scrollTop, scrollHeight, clientHeight } = element;
    shouldScroll = scrollTop + clientHeight >= scrollHeight - 5;
  }

  function formatTimestamp(timestamp) {
    const date = new Date(timestamp);
    return (
      date.getFullYear() +
      "-" +
      String(date.getMonth() + 1).padStart(2, "0") +
      "-" +
      String(date.getDate()).padStart(2, "0") +
      " " +
      String(date.getHours()).padStart(2, "0") +
      ":" +
      String(date.getMinutes()).padStart(2, "0") +
      ":" +
      String(date.getSeconds()).padStart(2, "0")
    );
  }
</script>

<div
  bind:this={element}
  on:scroll={handleScroll}
  class="h-48 overflow-y-auto bg-gray-800 p-4 font-mono text-sm text-white"
>
  {#each logs as log}
    <div
      class={classNames("mb-0.5 block text-xs", {
        "font-bold text-red-500": log.type === "error",
        "text-yellow-500": log.type === "warn",
        "bg-green-950 text-green-400": log.type === "success",
        "text-gray-100": log.type === "info",
        "text-gray-400": log.type === "comment",
      })}
    >
      <span class="mr-1 inline-block tracking-tighter text-gray-400">{formatTimestamp(log.timestamp)}:</span>
      <span class="inline-block">{log.message}</span>
    </div>
  {/each}
</div>
