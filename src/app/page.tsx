import CopyButton from '@/components/CopyButton';
import { designGradeCount, groupCounts, skills, tierCounts } from '@/lib/skills';

const INDEX_COMMAND = 'python3 scripts/build-skill-index.py';

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

          <div className="install">
            <div>
              <p className="install-label">After you install or remove a skill, refresh the index:</p>
              <code>{INDEX_COMMAND}</code>
            </div>
            <CopyButton value={INDEX_COMMAND} label="Copy command" />
          </div>
        </section>

        <section className="strip" aria-label="Catalogue at a glance">
          <div>
            <b>{total}</b>
            <span>installed skills</span>
          </div>
          {tiers.map((t) => (
            <div key={t.tier}>
              <b>{t.count}</b>
              <span>{t.tier}</span>
            </div>
          ))}
          <p className="note">
            Every grade is a design grade: {designs} of {total} skills, none validated against a model yet.
          </p>
        </section>

        <section className="new" aria-labelledby="new-title">
          <h2 id="new-title">New to skills?</h2>
          <div className="cards">
            <div className="card">
              <h3>What a skill is</h3>
              <p>A folder with a SKILL.md file, optional scripts, references and assets. Agents load it when it matches the task.</p>
            </div>
            <div className="card">
              <h3>Installing skills</h3>
              <p>Install the extension, then pick the skills for each project. Skills that need a licence key are marked by tier.</p>
            </div>
            <div className="card">
              <h3>How grades work</h3>
              <p>Each skill is scored on support, importance, severity, usage and presence. The grade sets its tier.</p>
            </div>
          </div>
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

      <footer>
        <p>Skill Atlas · the skills installed in this project · grades from the vscode-rlm registry.</p>
      </footer>
    </>
  );
}
