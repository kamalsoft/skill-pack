'use client';

import { useState, type FormEvent } from 'react';
import { atlasLink } from '@/lib/config';

/** Sends the search to the atlas, which filters its list by the query. */
export default function SearchForm() {
  const [query, setQuery] = useState('');

  function submit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const q = query.trim();
    window.location.href = q ? atlasLink({ q }) : atlasLink();
  }

  return (
    <form className="search" role="search" onSubmit={submit}>
      <label htmlFor="home-q" className="sr-only">Search skills</label>
      <input
        id="home-q"
        type="search"
        placeholder="Search by goal or name"
        autoComplete="off"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />
      <button type="submit">Search</button>
    </form>
  );
}
