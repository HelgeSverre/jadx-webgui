<script>
  import { onDestroy, onMount } from "svelte";
  import io from "socket.io-client";
  import { addLog, logLevels, openFile, project, search } from "./store.js";
  import FileList from "./components/FileList.svelte";
  import FileViewer from "./components/FileViewer.svelte";
  import Console from "./components/Console.svelte";
  import { CodeXml } from "lucide-svelte";
  import { createFileTree } from "./utils.js";

  const API_URL = "http://localhost:8080";

  let files = [];
  let socket;

  onMount(() => {
    connectSocket();
    listFiles();
  });

  onDestroy(() => {
    if (socket) socket.disconnect();
  });

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
      addLog(`Project created: ${data.project}`, "success");
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
      console.log("Decompilation complete:", data);
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

  $: tree = createFileTree(files.filter((file) => file.toLowerCase().includes($search.toLowerCase())));
</script>

<main class="flex h-screen flex-col bg-gray-100 dark:bg-gray-900">
  <header class="flex flex-row items-center justify-between bg-blue-900 p-2 leading-none text-white">
    <h1 class="inline-flex items-center gap-2 font-mono text-sm">
      <CodeXml size="16" />
      <span class="inline-block">APK Decompiler</span>
    </h1>

    {#if $project !== null}
      <h2 class="bg-black p-1 !font-sans">
        <span class="font-mono text-xs">Project:</span>
        <span class="font-mono text-xs text-gray-300">
          {$project.name}
        </span>
      </h2>
    {/if}

    <div class="flex flex-row items-center justify-end gap-2">
      <button
        class="inline-block h-6 cursor-pointer rounded px-2 py-0.5 text-sm font-medium text-blue-100 focus-within:bg-white focus-within:bg-opacity-25 hover:bg-white hover:bg-opacity-25 focus:outline-0"
        on:click={reset}
      >
        Reset environment
      </button>

      <label
        for="file-selector"
        class="inline-block h-6 cursor-pointer rounded px-2 py-0.5 text-sm font-medium text-blue-100 focus-within:bg-white focus-within:bg-opacity-25 hover:bg-white hover:bg-opacity-25"
      >
        Upload file
        <input id="file-selector" type="file" accept=".apk,.xapk" on:change={uploadFile} class="sr-only" />
      </label>
    </div>
  </header>

  <main class="flex flex-1 overflow-hidden">
    <aside class="w-72 border-r border-gray-800 bg-gray-200 dark:bg-gray-950">
      <input
        type="search"
        bind:value={$search}
        placeholder="Search files..."
        class="w-full border-b border-gray-800 bg-gray-100 p-2 font-mono text-xs dark:bg-gray-900 dark:text-white"
      />

      <div class="flex h-full flex-1 flex-col overflow-scroll bg-gray-200 pb-12 dark:bg-gray-900">
        <FileList forceExpand={$search.length} tree={tree} on:selectFile={(e) => getFileContent(e.detail)} />
      </div>
    </aside>

    <div class="flex w-full flex-1 overflow-auto">
      <FileViewer />
    </div>
  </main>

  <Console />
</main>
