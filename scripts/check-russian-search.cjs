'use strict';

// Exercise the production index with real Lunr, including the Cyrillic
// regression that returned no results through its default English pipeline.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { execFileSync } = require('node:child_process');

const project = path.resolve(__dirname, '..');
const publicDir = process.argv[2];
assert(publicDir, 'usage: node scripts/check-russian-search.cjs PUBLIC_DIR');
const moduleDir = execFileSync(
  'go', ['list', '-m', '-f', '{{.Dir}}', 'github.com/pgsty/oink'],
  { cwd: project, encoding: 'utf8' },
).trim();
global.window = {};
const lunr = require(path.join(moduleDir, 'assets/js/third_party/lunr.min.js'));
const local = require(path.join(project, 'assets/js/search-engine.js'));
const upstream = require(path.join(moduleDir, 'assets/js/search-engine.js'));
const indexes = fs.readdirSync(publicDir).filter(
  (name) => /^offline-search-index\.ru\..*\.json$/.test(name),
);
assert.equal(indexes.length, 1, 'exactly one Russian production index');
const documents = JSON.parse(fs.readFileSync(path.join(publicDir, indexes[0]), 'utf8'));
const engine = local.create(documents, lunr, 30);
const original = upstream.create(documents, lunr, 30);

for (const query of ['Восстановление', 'ВОССТАНОВЛЕНИЕ', 'резервное копирование']) {
  assert(engine.query(query).some(
    ({ doc }) => doc.ref.startsWith('/ru/docs/pgbackrest/'),
  ), `Russian pgBackRest results missing for ${query}`);
}
for (const [query, route] of [
  ['статистика', '/ru/docs/haproxy/statistics-and-monitoring/'],
  ['СТАТИСТИКА', '/ru/docs/haproxy/statistics-and-monitoring/'],
  ['ведение журнала', '/ru/docs/haproxy/configuration-logging/'],
  ['HAProxy', '/ru/docs/haproxy/'],
]) {
  assert(engine.query(query).some(({ doc }) => doc.ref === route),
    `HAProxy search result ${route} missing for ${query}`);
}
for (const query of ['pgBackRest', 'restore', 'backup', 'configuration']) {
  assert.deepEqual(engine.query(query), original.query(query),
    `Latin search changed for ${query}`);
}
console.log('Validated Cyrillic pgBackRest and HAProxy searches, technical HAProxy search and unchanged Latin results using the production index.');
