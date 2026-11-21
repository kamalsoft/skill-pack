import { designGradeCount, groupCounts, skills, tierCounts } from '@/lib/skills';


export default function Home() {
  const total = skills.length;
  const tiers = tierCounts();
  const groups = groupCounts();
  const designs = designGradeCount();

  return (
    <>
      <header className="topbar">
        <span className="brand">
          <span className="mark" aria-hidden="true" />
          Skill Atlas
        </span>
      </header>

      <main>
        <section className="hero">
          <p className="eyebrow">Skill Atlas · {total} skills installed</p>
          <h1>Every skill has a starting point. Find yours.</h1>
          <p className="lede">
            The skills installed in this project, grouped by family and graded A+ to D. Each skill has its steps, its grade
            and its folder.
          </p>
        </section>

        <section className="browse" aria-labelledby="browse-title">
          <h2 id="browse-title">Browse by group</h2>
          <div className="cards">
            {groups.map((g) => (
              <div key={g.id} className="card group">
                <b>{g.count}</b>
                <h3>{g.name}</h3>
              </div>
            ))}
          </div>
        </section>

      </main>
    </>
  );
}
