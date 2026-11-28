'use strict';

// Exercise the production search index with the shipped OINK search engine.
// OINK handles literal Unicode queries directly without an external stemmer,
// so the site uses the published engine without a local override.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { execFileSync } = require('node:child_process');
const project = path.resolve(__dirname, '..');
const publicDir = process.argv[2];
assert(publicDir, 'usage: node scripts/test-pgbackrest-search.cjs PUBLIC_DIR');
const moduleDir = JSON.parse(execFileSync(
  'go', ['mod', 'download', '-json', 'github.com/pgsty/oink'],
  { cwd: project, encoding: 'utf8' },
)).Dir;
assert(moduleDir, 'published OINK module must resolve to a directory');
global.window = {};
const upstream = require(path.join(moduleDir, 'assets/js/search-engine.js'));
const queries = {
  en: 'Weak Encryption', zh: '弱加密', fr: 'Sous-clés',
  ja: '脆弱', de: 'Unterschlüssel', ru: 'Слабые',
  ar: 'مفاتيح فرعية', es: 'Subclaves',
};
for (const [lang, query] of Object.entries(queries)) {
  const files = fs.readdirSync(publicDir).filter(
    name => name.startsWith(`offline-search-index.${lang}.`) && name.endsWith('.json'),
  );
  assert.equal(files.length, 1, `exactly one ${lang} index`);
  const documents = JSON.parse(fs.readFileSync(path.join(publicDir, files[0]), 'utf8'));
  const bodyFiles = fs.readdirSync(publicDir).filter(
    name => name.startsWith(`offline-search-body.${lang}.`) && name.endsWith('.json'),
  );
  if (bodyFiles.length === 1) {
    const byRef = new Map(documents.map(doc => [doc.ref, doc]));
    for (const item of JSON.parse(fs.readFileSync(path.join(publicDir, bodyFiles[0]), 'utf8'))) {
      const doc = byRef.get(item.ref);
      if (doc && typeof item.body === 'string') doc.body = item.body;
    }
  }
  const engine = upstream.create(documents, 12);
  const route = (lang === 'en' ? '' : '/' + lang) + '/pgbackrest/news/';
  for (const term of [query, query.toUpperCase()]) {
    assert(engine.query(term).some(({ doc }) => doc.ref === route),
      `${lang} security announcement missing for ${term}`);
  }
  if (lang === 'ru' || lang === 'ar') {
    const technical = lang === 'ru'
      ? [['Восстановление', 'резервное копирование'], '/ru/pgbackrest/']
      : [['النسخ الاحتياطي', 'الاسترداد'], `/${lang}/pgbackrest/`];
    for (const term of technical[0]) {
      assert(engine.query(term).some(({ doc }) => doc.ref.startsWith(technical[1])),
        `${lang} technical search missing for ${term}`);
    }
  }
  for (const term of ['pgBackRest', 'restore', 'backup', 'config', 'OpenSSL']) {
    const results = engine.query(term);
    assert(results.length > 0, `${lang}: Latin search returned no results for ${term}`);
    const prefix = lang === 'en' ? '/' : '/' + lang + '/';
    assert(results.every(({ doc }) => doc.ref.startsWith(prefix)),
      `${lang}: Latin query escaped its language index: ${term}`);
  }
}
console.log('Validated eight-language security-announcement search, Cyrillic/Arabic recovery queries, and Latin/CJK queries with the published OINK engine.');
