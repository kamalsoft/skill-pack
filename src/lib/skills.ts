import summary from '@/data/skills.json';

export type Tier = 'premium' | 'pro' | 'essentials';

/** One installed skill, as written by scripts/build-skill-index.py. */
export type Skill = {
  id: string;
  goal: string;
  family: string;
  tier: Tier;
  grade: string | null;
  design: boolean;
};

/** Families grouped as the atlas groups them. A family not listed here goes to "Other". */
export const GROUPS: { id: string; name: string; families: string[] }[] = [
  { id: 'software', name: 'Software', families: ['devops', 'techops', 'web', 'core'] },
  { id: 'ops', name: 'Operations', families: ['ops', 'pm', 'ind', 'mfg', 'ehs', 'qual'] },
  { id: 'business', name: 'Business', families: ['sales', 'mkt', 'neg', 'fin', 'cs'] },
  { id: 'people', name: 'People', families: ['hr', 'hrc'] },
  { id: 'legal', name: 'Legal and risk', families: ['legal'] },
];

export const skills: Skill[] = summary as Skill[];

export function groupOf(family: string): string {
  return GROUPS.find((g) => g.families.includes(family))?.id ?? 'other';
}

export type GroupCount = { id: string; name: string; count: number };

/** Skill counts per group, in the order of GROUPS, with Other last. */
export function groupCounts(): GroupCount[] {
  const counts = new Map<string, number>();
  for (const s of skills) counts.set(groupOf(s.family), (counts.get(groupOf(s.family)) ?? 0) + 1);
  const rows = GROUPS.map((g) => ({ id: g.id, name: g.name, count: counts.get(g.id) ?? 0 }));
  rows.push({ id: 'other', name: 'Other', count: counts.get('other') ?? 0 });
  return rows.filter((r) => r.count > 0);
}

export type TierCount = { tier: Tier; count: number };

export function tierCounts(): TierCount[] {
  return (['premium', 'pro', 'essentials'] as Tier[]).map((tier) => ({
    tier,
    count: skills.filter((s) => s.tier === tier).length,
  }));
}

export function designGradeCount(): number {
  return skills.filter((s) => s.grade && s.design).length;
}
