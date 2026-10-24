// Minimal IndexedDB key-value wrapper (one object store per kind of data, SPEC UI 4.2).
// Falls back to memory when IndexedDB is unavailable (private mode, tests).

export type StoreName = "drafts" | "resume" | "quiz_inflight" | "sample";
const STORES: StoreName[] = ["drafts", "resume", "quiz_inflight", "sample"];

export interface KeyValueStore<T> {
  get(key: string): Promise<T | undefined>;
  put(key: string, value: T): Promise<void>;
  delete(key: string): Promise<void>;
}

export class MemoryStore<T> implements KeyValueStore<T> {
  readonly data = new Map<string, T>();
  async get(key: string) {
    return this.data.get(key);
  }
  async put(key: string, value: T) {
    this.data.set(key, value);
  }
  async delete(key: string) {
    this.data.delete(key);
  }
}

let dbPromise: Promise<IDBDatabase> | null = null;

function openDb(): Promise<IDBDatabase> {
  dbPromise ??= new Promise((resolve, reject) => {
    const open = indexedDB.open("prep-app", 1);
    open.onupgradeneeded = () => {
      for (const name of STORES) {
        if (!open.result.objectStoreNames.contains(name)) open.result.createObjectStore(name);
      }
    };
    open.onsuccess = () => resolve(open.result);
    open.onerror = () => reject(open.error);
  });
  return dbPromise;
}

function promisify<R>(request: IDBRequest<R>): Promise<R> {
  return new Promise((resolve, reject) => {
    request.onsuccess = () => resolve(request.result);
    request.onerror = () => reject(request.error);
  });
}

export function idbStore<T>(name: StoreName): KeyValueStore<T> {
  if (typeof indexedDB === "undefined") return new MemoryStore<T>();
  return {
    async get(key) {
      const db = await openDb();
      return (await promisify(db.transaction(name).objectStore(name).get(key))) as T | undefined;
    },
    async put(key, value) {
      const db = await openDb();
      // strict durability: survive a power cut right after the write (Chrome defaults to relaxed)
      const tx = db.transaction(name, "readwrite", { durability: "strict" });
      tx.objectStore(name).put(value, key);
      await new Promise<void>((resolve, reject) => {
        tx.oncomplete = () => resolve();
        tx.onerror = () => reject(tx.error);
        tx.onabort = () => reject(tx.error);
      });
    },
    async delete(key) {
      const db = await openDb();
      const tx = db.transaction(name, "readwrite");
      tx.objectStore(name).delete(key);
      await new Promise<void>((resolve) => {
        tx.oncomplete = () => resolve();
      });
    },
  };
}
