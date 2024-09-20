import { writable } from "svelte/store";

// Utility to create a store that syncs with localStorage
export function persistentStore(key, initialValue = null) {
  const storedValue = localStorage.getItem(key);
  const parsedValue = storedValue ? JSON.parse(storedValue) : initialValue;

  const store = writable(parsedValue);

  store.subscribe((value) => {
    localStorage.setItem(key, JSON.stringify(value));
  });

  return store;
}
