import { existsSync, readFileSync, readdirSync } from "node:fs";
import { dirname, join, relative, resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const editions = ["claude", "chatgpt-agents"];
const expectedSkills = [
  "hono-stack",
  "jp-comm",
  "jp-requirement",
  "meo-pptx",
  "premium-web",
  "seo",
];

// `allowed-tools` pre-approves tools for the turn that invokes the skill — it does NOT
// restrict which tools are callable (every tool remains available; unlisted tools just go
// through the normal permission prompt). Verified against
// https://code.claude.com/docs/en/skills#pre-approve-tools-for-a-skill (fetched 2026-08-13).
// Owner's explicit decision (2026-08-13): scope each skill's grant to what its own
// documented workflow does, so running the skill doesn't stop for a prompt on every write/
// bash/fetch call it makes as part of normal use. Do not "fix" this back to a single minimal
// set for all six — that was tried and reverted once already; see
// SKILL-AUDIT-RECONCILIATION.md §R-02 for the full history.
const expectedAllowedTools = {
  "hono-stack": "Bash, Read, Write, Edit, AskUserQuestion, Skill", // scaffolds code, runs wrangler
  "jp-comm": "Read, Write, AskUserQuestion, Skill", // drafts text; rarely needs Bash/Edit
  "jp-requirement": "Read, Write, Edit, AskUserQuestion, Skill", // writes 要件定義書 to file
  "meo-pptx": "Bash, Read, Write, Edit, AskUserQuestion, Skill", // pptxgenjs, markitdown, render QA
  "premium-web": "Bash, Read, Write, Edit, AskUserQuestion, Skill", // builds site, measures PageSpeed
  seo: "Bash, Read, Write, Edit, WebFetch, AskUserQuestion, Skill", // curl raw HTML, read official docs
};

const errors = [];

function filesUnder(dir) {
  return readdirSync(dir, { withFileTypes: true }).flatMap((entry) => {
    const full = join(dir, entry.name);
    return entry.isDirectory() ? filesUnder(full) : [full];
  });
}

function frontmatter(text, file) {
  const lines = text.replace(/^\uFEFF/, "").split(/\r?\n/);
  if (lines[0] !== "---") {
    errors.push(`${file}: missing opening frontmatter delimiter`);
    return new Map();
  }
  const end = lines.indexOf("---", 1);
  if (end < 0) {
    errors.push(`${file}: missing closing frontmatter delimiter`);
    return new Map();
  }
  const fields = new Map();
  for (const line of lines.slice(1, end)) {
    const match = line.match(/^([A-Za-z][\w-]*):(?:\s*(.*))?$/);
    if (match) fields.set(match[1], match[2] ?? "");
  }
  return fields;
}

function descriptionValue(text) {
  const lines = text.replace(/^\uFEFF/, "").split(/\r?\n/);
  const end = lines.indexOf("---", 1);
  const start = lines.findIndex((line, index) => index > 0 && index < end && line.startsWith("description:"));
  if (start < 0) return "";
  const first = lines[start].slice("description:".length).replace(/^[ >|+-]+/, "").trim();
  const continuation = [];
  for (const line of lines.slice(start + 1, end)) {
    if (/^[A-Za-z][\w-]*:/.test(line)) break;
    continuation.push(line.trim());
  }
  return [first, ...continuation].filter(Boolean).join(" ");
}

function validateLinks(text, file) {
  for (const match of text.matchAll(/\[[^\]]*\]\(([^)]+)\)/g)) {
    const target = match[1].split("#", 1)[0].trim().replace(/^<|>$/g, "");
    if (!target || /^(?:https?:|mailto:|data:)/i.test(target)) continue;
    const decoded = decodeURIComponent(target);
    if (!existsSync(resolve(dirname(file), decoded))) {
      errors.push(`${file}: broken relative link ${target}`);
    }
  }
}

for (const edition of editions) {
  const editionDir = join(root, edition);
  const actualSkills = readdirSync(editionDir, { withFileTypes: true })
    .filter((entry) => entry.isDirectory())
    .map((entry) => entry.name)
    .sort();
  if (actualSkills.join("|") !== [...expectedSkills].sort().join("|")) {
    errors.push(`${edition}: skill folders differ from expected six`);
  }

  for (const skill of expectedSkills) {
    const skillFile = join(editionDir, skill, "SKILL.md");
    if (!existsSync(skillFile)) {
      errors.push(`${skillFile}: missing`);
      continue;
    }
    const text = readFileSync(skillFile, "utf8");
    const lineCount = text.split(/\r?\n/).length;
    if (lineCount > 500) errors.push(`${skillFile}: ${lineCount} lines; keep SKILL.md under 500`);

    const fields = frontmatter(text, skillFile);
    if (fields.get("name") !== skill) errors.push(`${skillFile}: name must match folder`);
    if (!fields.has("description")) errors.push(`${skillFile}: missing description`);
    if (!/^[a-z0-9-]{1,64}$/.test(skill)) errors.push(`${skillFile}: invalid skill name`);
    const description = descriptionValue(text);
    if (!description) errors.push(`${skillFile}: empty description`);
    if (description.length > 1024) errors.push(`${skillFile}: description exceeds 1024 characters`);

    const allowedFields = edition === "chatgpt-agents"
      ? new Set(["name", "description"])
      : new Set(["name", "description", "allowed-tools"]);
    for (const field of fields.keys()) {
      if (!allowedFields.has(field)) errors.push(`${skillFile}: unsupported frontmatter field ${field}`);
    }
    if (edition === "claude") {
      const expected = expectedAllowedTools[skill];
      if (!expected) {
        errors.push(`${skillFile}: no expected allowed-tools entry for skill "${skill}" in validate-skills.mjs`);
      } else if (fields.get("allowed-tools") !== expected) {
        errors.push(`${skillFile}: allowed-tools must be exactly "${expected}" (see expectedAllowedTools in this script)`);
      }
    }
    validateLinks(text, skillFile);
  }

  for (const file of filesUnder(editionDir).filter((path) => path.endsWith(".md"))) {
    const text = readFileSync(file, "utf8");
    validateLinks(text, file);
    const lines = text.split(/\r?\n/).length;
    if (!file.endsWith("SKILL.md") && lines > 100 && !/^## Mục lục$/m.test(text)) {
      errors.push(`${file}: reference over 100 lines needs a Mục lục`);
    }
  }
}

const claudeFiles = filesUnder(join(root, "claude"))
  .map((file) => relative(join(root, "claude"), file).replaceAll("\\", "/"))
  .sort();
const agentFiles = filesUnder(join(root, "chatgpt-agents"))
  .map((file) => relative(join(root, "chatgpt-agents"), file).replaceAll("\\", "/"))
  .sort();
if (claudeFiles.join("|") !== agentFiles.join("|")) {
  errors.push("edition file trees differ");
}

const allowedContentDiffs = new Set([
  ...expectedSkills.map((skill) => `${skill}/SKILL.md`),
  "meo-pptx/references/report-mode.md",
]);
const actualContentDiffs = new Set();
for (const rel of claudeFiles.filter((file) => agentFiles.includes(file))) {
  const left = readFileSync(join(root, "claude", rel));
  const right = readFileSync(join(root, "chatgpt-agents", rel));
  if (!left.equals(right)) {
    actualContentDiffs.add(rel);
    if (!allowedContentDiffs.has(rel)) errors.push(`${rel}: unexpected content drift between editions`);
  }
}
for (const rel of allowedContentDiffs) {
  if (!actualContentDiffs.has(rel)) errors.push(`${rel}: expected runtime delta is missing`);
}

const evalFile = join(root, "evals", "trigger-matrix.md");
if (!existsSync(evalFile)) {
  errors.push(`${evalFile}: missing forward-test matrix`);
} else {
  const evalText = readFileSync(evalFile, "utf8");
  for (const skill of expectedSkills) {
    const start = evalText.indexOf(`## \`${skill}\``);
    const end = start < 0 ? -1 : evalText.indexOf("\n## `", start + 1);
    const section = start < 0 ? "" : evalText.slice(start, end < 0 ? undefined : end);
    const counts = {
      Trigger: (section.match(/^\| Trigger \|/gm) ?? []).length,
      "Non-trigger": (section.match(/^\| Non-trigger \|/gm) ?? []).length,
      Boundary: (section.match(/^\| Boundary \|/gm) ?? []).length,
    };
    if (counts.Trigger !== 3 || counts["Non-trigger"] !== 2 || counts.Boundary !== 2) {
      errors.push(`${evalFile}: ${skill} needs exactly 3 trigger, 2 non-trigger, 2 boundary cases`);
    }
  }
}

const corpus = editions.map((edition) => filesUnder(join(root, edition))
  .filter((file) => file.endsWith(".md"))
  .map((file) => readFileSync(file, "utf8"))
  .join("\n")).join("\n");
for (const forbidden of [
  "Slide size:** A4",
  "thiếu 80%",
  "không cần quay lại tài liệu gốc",
  "User im lặng = đã đồng ý",
]) {
  if (corpus.includes(forbidden)) errors.push(`forbidden stale guidance remains: ${forbidden}`);
}

if (errors.length) {
  console.error(`Skill validation failed (${errors.length}):`);
  for (const error of errors) console.error(`- ${error}`);
  process.exit(1);
}

console.log("Skill validation passed: 2 editions, 6 skills, frontmatter, links, ToCs, sync, stale-rule checks.");
