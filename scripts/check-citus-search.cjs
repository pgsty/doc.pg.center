'use strict';

// Exercise the shipped OINK search engine against real bilingual indexes.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { execFileSync } = require('node:child_process');
const project = path.resolve(__dirname, '..');
const publicDir = process.argv[2];
assert(publicDir, 'usage: node scripts/check-citus-search.cjs PUBLIC_DIR');
const moduleDir = JSON.parse(execFileSync('go', ['mod', 'download', '-json', 'github.com/pgsty/oink'],
  { cwd: project, encoding: 'utf8' })).Dir;
global.window = {};
const lunr = require(path.join(moduleDir, 'assets/js/third_party/lunr.min.js'));
const search = require(path.join(moduleDir, 'assets/js/search-engine.js'));

for (const language of ['en', 'zh']) {
  const prefix = language === 'en' ? '/citus/' : '/zh/citus/';
  const files = fs.readdirSync(publicDir).filter(name =>
    name === `offline-search-index.${language}.json` ||
    (name.startsWith(`offline-search-index.${language}.`) && name.endsWith('.json')));
  assert.equal(files.length, 1, `one ${language} index`);
  const documents = JSON.parse(fs.readFileSync(path.join(publicDir, files[0]), 'utf8'));
  const collection = documents.filter(doc => doc.ref.startsWith(prefix));
  assert.equal(collection.length, 67, `all ${language} Citus pages indexed`);
  const engine = search.create(documents, lunr, 12);
  const queries = [
    ['create_distributed_table', 'reference/api-udf/#create_distributed_table'],
    ['citus.node_conninfo', 'reference/api-guc/#citusnode_conninfo-text'],
    [language === 'en' ? 'distribution column' : '分布列', 'overview/what-is-citus/#distribution-column'],
  ];
  for (const [query, target] of queries) {
    const results = engine.query(query, { root: collection[0].root });
    assert(results.some(result => result.ref === prefix + target), `${language}: missing anchored hit for ${query}`);
    assert(results.every(result => result.doc.ref.startsWith(prefix)), `${language}: search escaped Citus scope`);
    for (const result of results) {
      if (!result.ref.includes('#')) continue;
      const [route, id] = result.ref.split('#');
      const html = fs.readFileSync(path.join(publicDir, route, 'index.html'), 'utf8');
      const anchor = decodeURIComponent(id);
      assert(html.includes(`id="${anchor}"`) || html.includes(`id=${anchor}>`) || html.includes(`id=${anchor} `),
        `${language}: search anchor absent from HTML: ${result.ref}`);
    }
  }
}
console.log('Validated Citus English/Chinese scoped search, all 134 indexed pages, API names, and heading destinations.');
