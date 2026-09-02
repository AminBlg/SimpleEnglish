const assert = require('node:assert/strict');
const { spawnSync } = require('node:child_process');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const test = require('node:test');

const {
  FALLBACK_CONTEXT,
  MAX_CHARS,
  buildContext,
  promptCandidates,
  readFirstFile,
  stripFrontmatter,
} = require('./simple-english-activate');

const SCRIPT = path.join(__dirname, 'simple-english-activate.js');
const REPO_PROMPT = path.join(__dirname, '..', '..', 'prompts', 'system-prompt.md');

function tmpRoot(promptText) {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'se-hook-'));
  fs.mkdirSync(path.join(root, 'prompts'));
  if (promptText !== undefined) {
    fs.writeFileSync(path.join(root, 'prompts', 'system-prompt.md'), promptText);
  }
  return root;
}

function runHook(env) {
  return spawnSync(process.execPath, [SCRIPT], { env: { ...process.env, PLUGIN_ROOT: '', CLAUDE_PLUGIN_ROOT: '', ...env }, encoding: 'utf8' });
}

test('prefers the prompt under the plugin root', () => {
  assert.equal(promptCandidates('/plugin', '/plugin/src/hooks')[0], '/plugin/prompts/system-prompt.md');
});

test('falls back to the repository layout without a plugin root', () => {
  assert.equal(promptCandidates(undefined, '/repo/src/hooks')[0], '/repo/prompts/system-prompt.md');
});

test('skips an unreadable candidate and reads the next one', (t) => {
  if (process.getuid && process.getuid() === 0) {
    t.skip('root can read mode 000 files');
    return;
  }
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'se-read-'));
  const locked = path.join(dir, 'locked.md');
  const open = path.join(dir, 'open.md');
  fs.writeFileSync(locked, 'SECRET');
  fs.chmodSync(locked, 0o000);
  fs.writeFileSync(open, 'OPEN');
  assert.equal(readFirstFile([locked, open]), 'OPEN');
  fs.chmodSync(locked, 0o644);
});

test('skips a directory candidate', () => {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'se-dir-'));
  const asDir = path.join(dir, 'system-prompt.md');
  fs.mkdirSync(asDir);
  const file = path.join(dir, 'real.md');
  fs.writeFileSync(file, 'REAL');
  assert.equal(readFirstFile([asDir, file]), 'REAL');
});

test('returns an empty string when every candidate fails', () => {
  assert.equal(readFirstFile(['/nonexistent/a.md', '/nonexistent/b.md']), '');
});

test('removes YAML frontmatter with LF or CRLF line endings', () => {
  assert.equal(stripFrontmatter('---\nname: x\n---\nBody'), 'Body');
  assert.equal(stripFrontmatter('---\r\nname: x\r\n---\r\nBody'), 'Body');
});

test('uses the fallback ruleset when there is no prompt text', () => {
  assert.equal(buildContext(''), FALLBACK_CONTEXT);
});

test('the shipped prompt fits under the Claude Code stdout cap', () => {
  const out = buildContext(fs.readFileSync(REPO_PROMPT, 'utf8'));
  assert.ok(out.length <= MAX_CHARS, `${out.length} > ${MAX_CHARS}`);
  assert.ok(out.includes('THE REPLY'));
  assert.ok(out.startsWith('SIMPLE ENGLISH SKILL ACTIVE AUTOMATICALLY'));
});

test('an oversized prompt falls back instead of getting cut mid-sentence', () => {
  const out = buildContext('x'.repeat(MAX_CHARS + 1));
  assert.equal(out, FALLBACK_CONTEXT);
});

test('main() reads the prompt from CLAUDE_PLUGIN_ROOT', () => {
  const root = tmpRoot('CLAUDE-COPY');
  const r = runHook({ CLAUDE_PLUGIN_ROOT: root });
  assert.equal(r.status, 0);
  assert.ok(r.stdout.includes('CLAUDE-COPY'));
});

test('main() reads the prompt from PLUGIN_ROOT (Codex)', () => {
  const root = tmpRoot('CODEX-COPY');
  const r = runHook({ PLUGIN_ROOT: root });
  assert.equal(r.status, 0);
  assert.ok(r.stdout.includes('CODEX-COPY'));
});

test('main() exits 0 with the fallback when no candidate exists', () => {
  // Copy the script somewhere with no prompts/ nearby, so the repository
  // layout cannot rescue it, then point the plugin root at an empty tree.
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'se-main-'));
  const script = path.join(dir, 'a', 'b', 'hook.js');
  fs.mkdirSync(path.dirname(script), { recursive: true });
  fs.copyFileSync(SCRIPT, script);
  const root = tmpRoot(undefined);
  const r = spawnSync(process.execPath, [script], { env: { ...process.env, PLUGIN_ROOT: '', CLAUDE_PLUGIN_ROOT: root }, encoding: 'utf8' });
  assert.equal(r.status, 0);
  assert.equal(r.stdout, FALLBACK_CONTEXT);
});
