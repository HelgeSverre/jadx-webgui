<script>
  import { onMount } from "svelte";
  import io from "socket.io-client";
  import axios from "axios";
  import FileList from "./components/FileList.svelte";
  import FileViewer from "./components/FileViewer.svelte";
  import Console from "./components/Console.svelte";

  const API_URL = "http://localhost:8080";

  let search = "";
  let files = [];
  let selectedFile = "";
  let selectedFileContent = "";
  let logs = [];
  let socket;

  onMount(() => {
    socket = io(API_URL, {
      transports: ["websocket"],
      upgrade: false,
    });

    socket.on("connect", () => {
      addLog("[WS] Websocket connection established", "comment");
    });

    socket.on("console_output", (data) => {
      console.log(data);
      addLog(data.data);
    });

    socket.on("decompile_complete", (data) => {
      if (data.status === "success") {
        addLog("Decompilation completed successfully");
      } else {
        addLog("Decompilation failed");
      }

      listFiles();
    });

    listFiles();
  });

  function addLog(message, type = "info") {
    logs = [...logs, { message, type, timestamp: new Date() }];
  }

  function clearLogs() {
    logs = [];
  }

  function reset() {
    clearLogs();
    selectedFile = "";
    selectedFileContent = "";
    files = [];

    axios.delete(API_URL + "/wipe").then((res) => {
      if (res.data.folders.length === 0) {
        addLog("Nothing to wipe", "warn");
        return;
      }

      addLog("Wiped: " + res.data.folders.join(", "), "success");
    });
  }

  async function uploadFile(event) {
    const file = event.target.files[0];
    const formData = new FormData();

    formData.append("file", file);

    try {
      axios.post(API_URL + "/upload", formData);
      addLog("Decompilation started...", "info");
    } catch (error) {
      addLog("Error: " + error.response.data, "error");
    }
  }

  async function listFiles() {
    try {
      const response = await axios.get(API_URL + "/files");
      files = response.data.files;

      if (files.length === 0) {
        addLog("No files found");
      } else {
        addLog("Files list updated");
      }
    } catch (error) {
      addLog("Error: " + error, "error");
    }
  }

  async function getFileContent(file) {
    try {
      const response = await axios.get(API_URL + `/file/${encodeURIComponent(file)}`, {
        responseType: "text",
      });
      selectedFile = file;
      selectedFileContent = response.data;
      addLog(`Fetched file: ${file}`, "info");
    } catch (error) {
      if (error.response && error.response.status === 404) {
        addLog(`File not found: ${error.response.data.path}`, "warn");
      } else {
        addLog("An error occurred while fetching the file content", "error");
      }
    }
  }

  $: filteredFiles = files.filter((file) => file.toLowerCase().includes(search.toLowerCase()));
</script>

<main class="flex h-screen flex-col bg-gray-100">
  <header class="flex flex-row items-center justify-between bg-blue-900 p-2 leading-none text-white">
    <h1 class="font-mono text-sm">APK Decompiler</h1>

    <div class="ml-auto">
      <button class="rounded bg-white px-2 py-0.5 text-sm text-black hover:bg-opacity-75" on:click={reset}>
        Reset
      </button>

      <label
        for="file-selector"
        class="inline-block cursor-pointer rounded px-2 py-0.5 text-sm hover:bg-white hover:bg-opacity-25"
      >
        Upload file
      </label>
      <input id="file-selector" type="file" accept=".apk,.xapk" on:change={uploadFile} class="sr-only" />
    </div>
  </header>

  <div class="flex flex-1 overflow-hidden">
    <aside class="w-64 bg-gray-200">
      <input type="search" bind:value={search} placeholder="Search files..." class="w-full p-2 text-sm" />
      <FileList files={filteredFiles} on:selectFile={(event) => getFileContent(event.detail)} />
    </aside>

    <div class="flex-1 overflow-auto p-4">
      <FileViewer content={selectedFileContent} file={selectedFile} />
    </div>
  </div>

  <footer>
    <Console logs={logs} />
  </footer>
</main>

<style>
  :global(body) {
    margin: 0;
    font-family: Arial, sans-serif;
  }
</style>
