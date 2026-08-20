const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const test = require('node:test');

const {
  FALLBACK_CONTEXT,
  buildContext,
  readFirstFile,
  skillCandidates,
  stripFrontmatter,
} = require('./simple-english-activate');

test('prefers the skill in CLAUDE_PLUGIN_ROOT', () => {
  const candidates = skillCandidates('/plugin', '/plugin/src/hooks');

  assert.equal(candidates[0], '/plugin/skills/simple-english/SKILL.md');
});

test('accepts a Codex PLUGIN_ROOT', () => {
  const candidates = skillCandidates('/codex-plugin', '/codex-plugin/src/hooks');

  assert.equal(candidates[0], '/codex-plugin/skills/simple-english/SKILL.md');
});

test('supports a repository checkout without CLAUDE_PLUGIN_ROOT', () => {
  const candidates = skillCandidates(undefined, '/repo/src/hooks');

  assert.equal(candidates[0], '/repo/skills/simple-english/SKILL.md');
});

test('reads the first existing candidate', () => {
  const temporaryDirectory = fs.mkdtempSync(path.join(os.tmpdir(), 'simple-english-hook-'));
  const missing = path.join(temporaryDirectory, 'missing.md');
  const existing = path.join(temporaryDirectory, 'SKILL.md');
  fs.writeFileSync(existing, 'rules', 'utf8');

  assert.equal(readFirstFile([missing, existing]), 'rules');
});

test('removes YAML frontmatter with LF or CRLF line endings', () => {
  assert.equal(stripFrontmatter('---\nname: test\n---\nBody'), 'Body');
  assert.equal(stripFrontmatter('---\r\nname: test\r\n---\r\nBody'), 'Body');
});

test('injects the canonical skill body into hidden session context', () => {
  const context = buildContext('---\nname: simple-english\n---\n# Rules\nUse active voice.');

  assert.match(context, /^SIMPLE ENGLISH SKILL ACTIVE AUTOMATICALLY/);
  assert.match(context, /# Rules\nUse active voice\./);
  assert.doesNotMatch(context, /name: simple-english/);
});

test('uses a safe minimum ruleset when the skill file is unavailable', () => {
  assert.equal(buildContext(''), FALLBACK_CONTEXT);
});
