<script>
  import { Ban, CheckCheck, CircleHelp, Hourglass, Loader2 } from "lucide-svelte";
  import classNames from "classnames";

  export let apiKey = "";

  let status = "idle";

  async function checkApiKey() {
    if (!apiKey) {
      status = "missing ";
      return;
    }

    status = "checking";

    try {
      const response = await fetch(`https://identitytoolkit.googleapis.com/v1/accounts:signUp?key=${apiKey}`, {
        method: "POST",
        body: JSON.stringify({
          returnSecureToken: true,
        }),
        headers: {
          "Content-Type": "application/json",
        },
      });

      const data = await response.json();

      if (response.ok) {
        status = "error";
      } else if (data.error && data.error.message === "API key not valid. Please pass a valid API key.") {
        status = "error";
      } else if (data.error && data.error.message.includes("ADMIN_ONLY_OPERATION")) {
        status = "success";
      } else {
        status = "error";
      }
    } catch (error) {
      status = "error";
    }
  }
</script>

<button
  on:click={checkApiKey}
  class="inline-block transform-gpu items-center justify-center overflow-hidden rounded-full text-gray-900 duration-200 ease-in-out"
>
  {#if status === "idle"}
    <div class="border-gray-500 bg-gray-100 p-1 text-gray-700" role="alert">
      <Hourglass class="block size-4" />
    </div>
  {:else if status === "unchecked" || status === "checking"}
    <div class="border-blue-500 bg-blue-100 p-1 text-blue-700" role="alert">
      <Loader2 class={classNames("block size-4", { "animate-spin": status === "checking" })} />
    </div>
  {:else if status === "success"}
    <div class="border-green-500 bg-green-100 p-1 text-green-700" role="alert">
      <CheckCheck class="block size-4" />
    </div>
  {:else if status === "missing"}
    <div class="border-green-500 bg-green-100 p-1 text-green-700" role="alert">
      <CircleHelp class="block size-4" />
    </div>
  {:else if status === "error"}
    <div class="border-red-500 bg-red-100 p-1 text-red-700" role="alert">
      <Ban class="block size-4" />
    </div>
  {/if}
</button>
