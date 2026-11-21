'use client';

import { useState } from 'react';

/** Copies a value to the clipboard and shows a short confirmation. */
export default function CopyButton({ value, label = 'Copy' }: { value: string; label?: string }) {
  const [done, setDone] = useState(false);

  async function copy() {
    try {
      await navigator.clipboard.writeText(value);
      setDone(true);
      setTimeout(() => setDone(false), 1600);
    } catch {
      setDone(false);
    }
  }

  return (
    <button type="button" className="copy-btn" onClick={copy} aria-live="polite">
      {done ? 'Copied' : label}
    </button>
  );
}
