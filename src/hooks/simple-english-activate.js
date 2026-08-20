#!/usr/bin/env node

const fs = require('node:fs');
const path = require('node:path');

const FALLBACK_CONTEXT = `SIMPLE ENGLISH SKILL ACTIVE AUTOMATICALLY

Apply ASD-STE100 Simplified Technical English to technical-writing tasks. Use short sentences, active voice, one term for one meaning, and conditions before commands. Do not change code, identifiers, commands, or quoted errors.`;

function skillCandidates(pluginRoot, hookDirectory) {
  const candidates = [];

  if (pluginRoot) {
    candidates.push(path.join(pluginRoot, 'skills', 'simple-english', 'SKILL.md'));
  }

  candidates.push(
    path.join(hookDirectory, '..', '..', 'skills', 'simple-english', 'SKILL.md'),
    path.join(hookDirectory, '..', 'skills', 'simple-english', 'SKILL.md'),
  );

  return candidates;
}

function readFirstFile(candidates) {
  for (const candidate of candidates) {
    try {
      return fs.readFileSync(candidate, 'utf8');
    } catch (error) {
      if (error.code !== 'ENOENT' && error.code !== 'ENOTDIR') {
        throw error;
      }
    }
  }

  return '';
}

function stripFrontmatter(content) {
  return content.replace(/^---\r?\n[\s\S]*?\r?\n---\r?\n?/, '');
}

function buildContext(skillContent) {
  if (!skillContent) {
    return FALLBACK_CONTEXT;
  }

  return [
    'SIMPLE ENGLISH SKILL ACTIVE AUTOMATICALLY',
    '',
    'Use the following skill without waiting for the user to name or invoke it. Keep its scope, modes, and exceptions authoritative.',
    '',
    stripFrontmatter(skillContent).trim(),
  ].join('\n');
}

function main() {
  const pluginRoot = process.env.PLUGIN_ROOT || process.env.CLAUDE_PLUGIN_ROOT;
  const candidates = skillCandidates(pluginRoot, __dirname);
  const skillContent = readFirstFile(candidates);
  process.stdout.write(buildContext(skillContent));
}

if (require.main === module) {
  main();
}

module.exports = {
  FALLBACK_CONTEXT,
  buildContext,
  readFirstFile,
  skillCandidates,
  stripFrontmatter,
};
