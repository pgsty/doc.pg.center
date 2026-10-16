'use strict';

// Exercise the production search index with real Lunr. The English pipeline
// drops Cyrillic; the local override must retain these queries and leave all
// existing Latin/CJK results unchanged.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { execFileSync } = require('node:child_process');
const project = path.resolve(__dirname, '..');
const publicDir = process.argv[2];
assert(publicDir, 'usage: node scripts/test-pgbackrest-search.cjs PUBLIC_DIR');
const moduleDir = execFileSync(
  'go', ['list', '-m', '-f', '{{.Dir}}', 'github.com/pgsty/oink'],
  { cwd: project, encoding: 'utf8' },
).trim();
global.window = {};
const lunr = require(path.join(moduleDir, 'assets/js/third_party/lunr.min.js'));
const local = require(path.join(project, 'assets/js/search-engine.js'));
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
  const engine = local.create(documents, lunr, 12);
  const original = upstream.create(documents, lunr, 12);
  const route = (lang === 'en' ? '' : '/' + lang) + '/pgbackrest/news/';
  for (const term of [query, query.toUpperCase()]) {
    assert(engine.query(term).some(({ doc }) => doc.ref === route),
      `${lang} security announcement missing for ${term}`);
  }
  if (lang === 'ru' || lang === 'ar') {
    assert(!original.query(query).some(({ doc }) => doc.ref === route),
      `${lang} upstream regression must be reproduced`);
    const technical = lang === 'ru'
      ? [['Восстановление', 'резервное копирование'], '/ru/pgbackrest/']
      : [['النسخ الاحتياطي', 'الاسترداد'], `/${lang}/pgbackrest/`];
    for (const term of technical[0]) {
      assert(engine.query(term).some(({ doc }) => doc.ref.startsWith(technical[1])),
        `${lang} technical search missing for ${term}`);
    }
  } else {
    assert.deepEqual(engine.query(query), original.query(query),
      `${lang} search behavior changed`);
  }
  for (const term of ['pgBackRest', 'restore', 'backup', 'configuration', 'OpenSSL']) {
    assert.deepEqual(engine.query(term), original.query(term),
      `${lang}: Latin search changed for ${term}`);
  }
}
console.log('Validated eight-language security-announcement search, Cyrillic/Arabic recovery queries, and unchanged Latin/CJK results.');
