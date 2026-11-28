'use strict';

// Exercise the production index with the shipped OINK search engine, including
// Cyrillic queries alongside Latin technical terms.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { execFileSync } = require('node:child_process');

const project = path.resolve(__dirname, '..');
const publicDir = process.argv[2];
assert(publicDir, 'usage: node scripts/check-russian-search.cjs PUBLIC_DIR');
const moduleDir = JSON.parse(execFileSync(
  'go', ['mod', 'download', '-json', 'github.com/pgsty/oink'],
  { cwd: project, encoding: 'utf8' },
)).Dir;
assert(moduleDir, 'published OINK module must resolve to a directory');
global.window = {};
const upstream = require(path.join(moduleDir, 'assets/js/search-engine.js'));
const indexes = fs.readdirSync(publicDir).filter(
  (name) => /^offline-search-index\.ru\..*\.json$/.test(name),
);
assert.equal(indexes.length, 1, 'exactly one Russian production index');
const documents = JSON.parse(fs.readFileSync(path.join(publicDir, indexes[0]), 'utf8'));
const bodyFiles = fs.readdirSync(publicDir).filter(
  (name) => /^offline-search-body\.ru\..*\.json$/.test(name),
);
if (bodyFiles.length === 1) {
  const byRef = new Map(documents.map((doc) => [doc.ref, doc]));
  for (const item of JSON.parse(fs.readFileSync(path.join(publicDir, bodyFiles[0]), 'utf8'))) {
    const doc = byRef.get(item.ref);
    if (doc && typeof item.body === 'string') doc.body = item.body;
  }
}
const engine = upstream.create(documents, 30);

for (const query of ['Восстановление', 'ВОССТАНОВЛЕНИЕ', 'резервное копирование']) {
  assert(engine.query(query).some(
    ({ doc }) => doc.ref.startsWith('/ru/pgbackrest/'),
  ), `Russian pgBackRest results missing for ${query}`);
}
for (const [query, route] of [
  ['статистика', '/ru/haproxy/statistics-and-monitoring/'],
  ['СТАТИСТИКА', '/ru/haproxy/statistics-and-monitoring/'],
  ['ведение журнала', '/ru/haproxy/configuration-logging/'],
  ['HAProxy', '/ru/haproxy/'],
]) {
  assert(engine.query(query).some(({ doc }) => doc.ref === route),
    `HAProxy search result ${route} missing for ${query}`);
}
for (const query of ['pgBackRest', 'restore', 'backup', 'config']) {
  const results = engine.query(query);
  assert(results.length > 0, `Latin search returned no results for ${query}`);
  assert(results.every(({ doc }) => doc.ref.startsWith('/ru/')),
    `Latin query escaped the Russian index: ${query}`);
}
console.log('Validated Cyrillic pgBackRest and HAProxy searches, technical HAProxy search and Latin queries using the production index.');
