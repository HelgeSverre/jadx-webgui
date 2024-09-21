import { persistentStore } from "./utils.js";

export const search = persistentStore("search", "");
export const logs = persistentStore("log", []);
export const expandedNodes = persistentStore("expandedNodes", []);

export function toggleNode(node) {
  expandedNodes.update((value) => {
    if (value.includes(node)) {
      return value.filter((n) => n !== node);
    }
    return [...value, node];
  });
}

export const logLevels = ["info", "warn", "error", "success", "debug", "comment", "note"];

/**
 * Add a log message to the log store
 *
 * @param {string} message - The message to log
 * @param {string} [type="info", "warn", "error", "success", "debug", "comment", "note"] - The type of log message
 */
export function addLog(message, type = "info") {
  logs.update((value) => [
    ...value,
    {
      type,
      message,
      timestamp: new Date().toISOString(),
    },
  ]);
}

export function clearLogs() {
  logs.update(() => []);
}
