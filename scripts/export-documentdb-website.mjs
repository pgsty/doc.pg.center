#!/usr/bin/env node
/** Export the Markdown actually served by the pinned DocumentDB website.
 * Usage: node scripts/export-documentdb-website.mjs DOCS_CHECKOUT WEBSITE_CHECKOUT OUTPUT.json
 * Node 22.13+; run npm ci in the external website checkout first. No builds,
 * install commands from the documentation, or source-tree writes are performed.
 */
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {execFileSync} from 'node:child_process';
import {createRequire, stripTypeScriptTypes} from 'node:module';
import {pathToFileURL} from 'node:url';
import {createHash} from 'node:crypto';

const [docsArg, websiteArg, outputArg] = process.argv.slice(2);
if (!docsArg || !websiteArg || !outputArg) {
  throw new Error('Provide DOCS_CHECKOUT WEBSITE_CHECKOUT OUTPUT.json');
}
const docs = path.resolve(docsArg), website = path.resolve(websiteArg), output = path.resolve(outputArg);
const revision = dir => execFileSync('git', ['-C', dir, 'rev-parse', 'HEAD'], {encoding:'utf8'}).trim();
const docsCommit = revision(docs), websiteCommit = revision(website);
if (docsCommit !== 'cf69384e6da9524cc0fc723e8ac5b6c0689af432' || websiteCommit !== '90cfa088351557cd618034dfc00ab817c35a5f76') {
  throw new Error('Check out the pinned revisions before exporting. Review new revisions before updating the importer.');
}
const stage = fs.mkdtempSync(path.join(os.tmpdir(), 'documentdb-export-'));
const requireWebsite = createRequire(path.join(website, 'package.json'));
for (const relative of ['app/services/articleService','app/lib/packageInstall','app/lib/docsAnchors','app/services/externalLinks']) {
  let source = fs.readFileSync(path.join(website, relative+'.ts'), 'utf8');
  // These two upstream imports are types without the `type` keyword.
  source = source.replace(/^import \{ (Article|Link) \} from [^;]+;$/gm, '');
  source = stripTypeScriptTypes(source);
  source = source.replace(/from (['"])([^'"]+)\1/g, (_, quote, specifier) => {
    const resolved = specifier.startsWith('.') ? specifier+'.mjs' :
      ['fs','path'].includes(specifier) ? 'node:'+specifier : pathToFileURL(requireWebsite.resolve(specifier)).href;
    return `from ${quote}${resolved}${quote}`;
  });
  const dest = path.join(stage, relative+'.mjs');
  fs.mkdirSync(path.dirname(dest), {recursive:true});
  fs.writeFileSync(dest, source);
}
for (const entry of fs.readdirSync(docs, {withFileTypes:true})) {
  if (entry.isDirectory() && fs.existsSync(path.join(docs, entry.name, 'navigation.yml'))) {
    fs.cpSync(path.join(docs, entry.name), path.join(stage, 'articles', entry.name), {recursive:true});
  }
}
process.chdir(stage);
const service = await import(pathToFileURL(path.join(stage, 'app/services/articleService.mjs')).href);
const articles = service.getAllArticlePaths().map(({section,slug}) => service.getArticleByPath(section,slug));
const pageSource = 'app/docs/[section]/[[...slug]]/page.tsx';
const pageText = fs.readFileSync(path.join(website, pageSource), 'utf8');
const commandMatch = pageText.match(/const dockerQuickRunCommand = `([^`]+)`;/);
if (!commandMatch || commandMatch[1].includes('${')) {
  throw new Error('Review the website installation primer before changing the export.');
}
// The TS template escapes the shell continuation backslash. Export its value.
const dockerCommand = commandMatch[1].replace(/\\\\/g, '\\');
const page_components = {
  source: pageSource,
  sha256: createHash('sha256').update(pageText).digest('hex'),
  docker_command: dockerCommand,
};
fs.writeFileSync(output, JSON.stringify({docs_commit:docsCommit, website_commit:websiteCommit, page_components, articles}, null, 2)+'\n');
console.log(`Exported ${articles.length} website articles to ${output}; staging retained at ${stage}`);
