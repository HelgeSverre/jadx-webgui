<script>
  import { onDestroy, onMount } from "svelte";
  import io from "socket.io-client";
  import { addLog, logLevels, openFile, project, search, settings } from "./store.js";
  import FileList from "./components/FileList.svelte";
  import FileViewer from "./components/FileViewer.svelte";
  import Console from "./components/Console.svelte";
  import { CodeXml } from "lucide-svelte";
  import { createFileTree } from "./utils.js";
  import FirebaseKeys from "./components/FirebaseKeys.svelte";
  import UrlList from "./components/UrlList.svelte";
  import classNames from "classnames";

  const API_URL = "http://localhost:8080";

  let files = [];
  let socket;
  let firebaseKeys = [];
  let endpoints = [];

  onMount(() => {
    connectSocket();
    listFiles();
  });

  onDestroy(() => {
    if (socket) socket.disconnect();
  });

  $: if ($project && $project.id) {
    fetchFirebaseKeys($project.id);
    fetchEndpoints($project.id);
  }

  function connectSocket() {
    socket = io(API_URL, {
      transports: ["websocket"],
      upgrade: false,
      reconnection: true,
      reconnectionAttempts: 5,
      timeout: 5000,
      autoConnect: true,
    });

    socket.on("connect", () => {
      addLog("WebSocket connection established", "success");
    });

    socket.on("project_created", (data) => {
      addLog(`Project created: ${data.project_id}`, "success");
      project.update((p) => {
        return {
          ...p,
          pending: false,
          id: data.project_id,
        };
      });
    });

    socket.on("disconnect", (reason) => {
      addLog(`Disconnected: ${reason}`, "debug");
    });

    socket.on("connect_error", (error) => {
      addLog(`Connection error: ${error.message}`, "error");
    });

    socket.on("console_output", (data) => {
      let type = "info";
      let msg = data.data;

      try {
        const [extractedType, ...rest] = data.data.split("-").map((str) => str.trim());
        const lowerCaseType = extractedType.toLowerCase();

        if (logLevels.includes(lowerCaseType)) {
          type = lowerCaseType;
          msg = rest.join("-").trim(); // Strip out the log level
        }

        if (data.type) {
          type = data.type;
        }
      } catch (error) {
        console.error("Error processing console output: ", error);
      }

      addLog(msg, type);
    });

    socket.on("decompile_complete", (data) => {
      if (data.status === "success") {
        addLog("Decompilation completed successfully", "success");
      } else {
        addLog("Decompilation failed", "error");
      }

      listFiles();
    });
  }

  function reset() {
    fetch(API_URL + "/wipe", { method: "DELETE" })
      .then((response) => response.json())
      .then((data) => {
        addLog("Resetting environment...", "info");
        openFile.update(() => null);
        search.update(() => "");
        files = [];

        project.update(() => null);

        if (data.folders.length === 0) {
          addLog("Project folder was empty, no files to wipe", "comment");
        } else {
          addLog("Removed all files and folders", "comment");
        }

        addLog("Environment reset", "success");
      })
      .catch((error) => {
        addLog("Error: " + error.message, "error");
      });
  }

  async function uploadFile(event) {
    const file = event.target.files[0];
    const formData = new FormData();

    formData.append("file", file);

    project.update(() => {
      return {
        name: file.name,
        size: file.size,
        type: file.type,
        pending: true,
      };
    });

    try {
      const response = await fetch(API_URL + "/upload", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      addLog("Decompilation started...", "info");
    } catch (error) {
      addLog("Error: " + error.message, "error");
    }
  }

  async function fetchFirebaseKeys(projectId) {
    try {
      const response = await fetch(`${API_URL}/firebase_keys/${projectId}`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      firebaseKeys = await response.json();
      addLog(`Fetched ${firebaseKeys.length} Firebase keys`, "info");
    } catch (error) {
      addLog("Error fetching Firebase keys: " + error.message, "error");
    }
  }

  async function fetchEndpoints(projectId) {
    try {
      const response = await fetch(`${API_URL}/endpoints/${projectId}`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      endpoints = await response.json();
      addLog(`Fetched ${endpoints.length} endpoints`, "info");
    } catch (error) {
      addLog("Error fetching endpoints: " + error.message, "error");
    }
  }

  async function listFiles() {
    try {
      const response = await fetch(API_URL + "/files");
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      files = data.files;

      if (files.length === 0) {
        addLog("Project folder is empty", "comment");
      } else {
        addLog("Project folder scanned", "info");
      }
    } catch (error) {
      addLog("An error occurred: " + error.message, "error");
    }
  }

  async function getFileContent(file) {
    try {
      const response = await fetch(API_URL + `/file/${encodeURIComponent(file)}`);
      if (!response.ok) {
        if (response.status === 404) {
          throw new Error(`File not found: ${file}`);
        }
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const content = await response.text();

      openFile.update(() => {
        return {
          file: file,
          content: content,
        };
      });

      addLog(`Fetched file: ${file}`, "info");
    } catch (error) {
      if (error.message.startsWith("File not found:")) {
        addLog(error.message, "warn");
      } else {
        addLog("An error occurred while fetching the file content", "error");
      }
    }
  }

  function handleKeyBindings(event) {
    if (event.key === "Escape") {
      openFile.update(() => null);
    }

    // command 2 - toggle console visibility
    if (event.metaKey && event.key === "2") {
      $settings.consoleCollapsed = !$settings.consoleCollapsed;
      event.preventDefault();
    }
  }

  $: tree = createFileTree(files.filter((file) => file.toLowerCase().includes($search.toLowerCase())));
</script>

<svelte:window on:keydown={handleKeyBindings} />

<main class="flex h-screen flex-col bg-zinc-900">
  <header class="flex flex-row items-center justify-between gap-4 bg-zinc-800 p-2 text-white">
    <h1 class="inline-flex items-center gap-2 font-mono text-sm">
      <CodeXml size="16" />
      <span class="inline-block">APK Decompiler</span>
    </h1>

    {#if $project !== null}
      <h2
        class="mr-auto rounded bg-zinc-700 bg-gradient-to-tr from-gray-700 to-gray-600 px-1.5 py-0.5 font-sans leading-none"
      >
        <span class="inline-block font-mono text-xs text-zinc-300">
          {$project.name}
        </span>
      </h2>
    {/if}

    <div class="flex flex-row items-center justify-end gap-2">
      <button
        class="inline-block h-6 cursor-pointer rounded bg-blue-600 px-2 py-0.5 text-sm font-medium text-white hover:bg-blue-500 focus:outline-0"
        on:click={reset}
      >
        Reset environment
      </button>

      <label
        for="file-selector"
        class="inline-block h-6 cursor-pointer rounded bg-blue-600 px-2 py-0.5 text-sm font-medium text-white hover:bg-blue-500"
      >
        Upload file
        <input id="file-selector" type="file" accept=".apk,.xapk" on:change={uploadFile} class="sr-only" />
      </label>
    </div>
  </header>

  <main class="flex flex-1 overflow-hidden">
    <aside class="bg-zinc-850 h-8 h-full w-72 shrink-0">
      <input
        type="search"
        bind:value={$search}
        placeholder="Search files..."
        class="w-full border-b border-zinc-700 bg-zinc-900 p-2 font-mono text-xs text-white"
      />

      <div class=" bg-zinc-850 flex h-full flex-1 flex-col overflow-scroll pb-12">
        <FileList forceExpand={$search.length} tree={tree} on:selectFile={(e) => getFileContent(e.detail)} />
      </div>
    </aside>

    <div class="flex w-full flex-1 flex-col pb-px">
      <div class="flex h-8 flex-row border-b border-zinc-700 bg-zinc-900">
        <button
          class={classNames("ml-auto block p-1 px-2 text-xs", {
            "bg-zinc-800 text-zinc-300": $settings.activeTab === "file",
            "bg-zinc-900 text-zinc-500": $settings.activeTab !== "file",
          })}
          on:click={() => ($settings.activeTab = "file")}
        >
          File Viewer
        </button>

        <button
          class={classNames("block p-1 px-2 text-xs", {
            "bg-zinc-800 text-zinc-300": $settings.activeTab === "firebase",
            "bg-zinc-900 text-zinc-500": $settings.activeTab !== "firebase",
          })}
          on:click={() => ($settings.activeTab = "firebase")}
        >
          Firebase Keys
        </button>
        <button
          class={classNames("block p-1 px-2 text-xs", {
            "bg-zinc-800 text-zinc-300": $settings.activeTab === "urls",
            "bg-zinc-900 text-zinc-500": $settings.activeTab !== "urls",
          })}
          on:click={() => ($settings.activeTab = "urls")}
        >
          URL Results
        </button>
      </div>
      <div class="flex min-h-0 flex-1 bg-zinc-900">
        {#if $settings.activeTab === "file"}
          <FileViewer />
        {:else if $settings.activeTab === "firebase"}
          <FirebaseKeys firebaseKeys={firebaseKeys} />
        {:else if $settings.activeTab === "urls"}
          <UrlList endpoints={endpoints} />
        {/if}
      </div>
    </div>
  </main>

  <Console />
</main>
