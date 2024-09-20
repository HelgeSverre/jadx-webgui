import { writable } from "svelte/store";

/**
 * A writable store that persists to local storage.
 *
 * @param key {string} The key to use in local storage.
 * @param initialValue {*} The initial value of the store.
 * @returns {Writable<*>} The writable store.
 */
export function persistentStore(key, initialValue = null) {
  const storedValue = localStorage.getItem(key);
  const parsedValue = storedValue ? JSON.parse(storedValue) : initialValue;

  const store = writable(parsedValue);

  store.subscribe((value) => {
    localStorage.setItem(key, JSON.stringify(value));
  });

  return store;
}

/**
 * Format a timestamp as a string.
 * @param {number} timestamp
 * @returns {string} The formatted timestamp. in the format "YYYY-MM-DD HH:MM:SS.mmm" e.g. "2021-08-01 12:34:56.789"
 */
export function formatTimestamp(timestamp) {
  const date = new Date(timestamp);
  return (
    date.getFullYear() +
    "." +
    String(date.getMonth() + 1).padStart(2, "0") +
    "." +
    String(date.getDate()).padStart(2, "0") +
    " " +
    String(date.getHours()).padStart(2, "0") +
    ":" +
    String(date.getMinutes()).padStart(2, "0") +
    ":" +
    String(date.getSeconds()).padStart(2, "0") +
    "." +
    String(date.getMilliseconds()).padStart(3, "0")
  );
}

/**
 * @typedef {Object} FileTreeNode
 * @property {string} type - The type of the node, either "directory" or "file".
 * @property {string} name - The name of the node.
 * @property {string} path - The path of the node.
 * @property {Object|undefined} children - The children of the node, if it's a directory.
 */

/**
 *
 *
 * @param {string[]} paths
 * @returns {FileTreeNode} The file tree.
 */
export function createFileTree(paths) {
  const tree = {};

  for (const path of paths) {
    const parts = path.split("/");
    let currentLevel = tree;

    for (let i = 0; i < parts.length; i++) {
      const part = parts[i];
      if (i === parts.length - 1) {
        // It's a file
        currentLevel[part] = {
          type: "file",
          name: part,
          path,
        };
      } else {
        // It's a directory
        if (!currentLevel[part]) {
          currentLevel[part] = {
            type: "directory",
            name: part,
            children: {},
            path,
          };
        }
        currentLevel = currentLevel[part].children;
      }
    }
  }

  return tree;
}
