/** The path the site is published under, for example "/skillpack" on GitHub Pages, or "" locally. */
export const BASE_PATH: string = process.env.NEXT_PUBLIC_BASE_PATH ?? '';

/** The skill atlas page, which is still the static page in public/atlas.html. */
export const ATLAS_HREF = `${BASE_PATH}/atlas.html`;

export function atlasLink(params: Record<string, string> = {}, hash = ''): string {
  const query = new URLSearchParams(params).toString();
  return `${ATLAS_HREF}${query ? `?${query}` : ''}${hash}`;
}
