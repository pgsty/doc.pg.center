#!/usr/bin/env node
// PLAYWRIGHT_MODULE=/external/playwright CHROME_EXECUTABLE=/external/chrome
// node scripts/check-etcd-browser.cjs BASE_URL EXTERNAL_OUTPUT_DIR
// Uses an isolated browser profile and an existing local production build.
const {chromium} = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const fs = require('fs');
const assert = require('assert/strict');
const base = (process.argv[2] || '').replace(/\/$/, '');
const output = process.argv[3];
assert(base && output, 'usage: BASE_URL EXTERNAL_OUTPUT_DIR');
fs.mkdirSync(output, {recursive: true});
const languages = {en:'en-US', zh:'zh-CN', fr:'fr-FR', ja:'ja-JP', de:'de-DE', ru:'ru-RU'};
const report = {status:'running', views:[], errors:[]};
const flatten = node => [node, ...(node.children || []).flatMap(flatten)];
async function visible(page, selector, action) {
  const locators = page.locator(selector);
  for (let i = 0; i < await locators.count(); i++) {
    if (await locators.nth(i).isVisible()) return locators.nth(i)[action]();
  }
  throw new Error('No visible control: ' + selector);
}
async function checkLocale(browser, language, htmlLanguage, viewport) {
  const context = await browser.newContext({viewport, reducedMotion:'reduce'});
  const page = await context.newPage();
  const row = {language, viewport, pages:[], interactions:[], imageReloads:[], errors:[]};
  report.views.push(row);
  await page.route(/https:\/\/(?:giscus\.app|(?:www\.)?google-analytics\.com|www\.googletagmanager\.com)\//,
                   route => route.fulfill({status:204, body:''}));
  page.on('pageerror', e => row.errors.push(String(e)));
  page.on('response', r => {if (r.status() >= 400 && r.url().startsWith(base)) row.errors.push(r.status() + ' ' + r.url());});
  try {
    const prefix = language === 'en' ? '' : '/' + language;
    const nav = await (await context.request.get(base + prefix + '/navigation.json')).json();
    const routes = flatten(nav.root).filter(n => n.id.startsWith('/docs/etcd/')).map(n => new URL(n.url).pathname);
    assert.equal(routes.length, 99);
    for (const [index, route] of routes.entries()) {
      await page.goto(base + route, {waitUntil:'load'});
      await page.locator('.td-content h1').first().waitFor({state:'visible'});
      const contentImages = page.locator('.td-content img');
      await contentImages.evaluateAll(images => images.forEach(img => {img.loading = 'eager';}));
      for (let i = 0; i < await contentImages.count(); i++) {
        const img = contentImages.nth(i);
        // Force image fetching for asset QA even for images below the fold.
        const waitImage = () => img.evaluate(img => new Promise((resolve, reject) => {
          let stopped = false;
          const deadline = setTimeout(() => {stopped = true; reject(new Error('image load timed out ' + (img.currentSrc || img.dataset.src)));}, 30000);
          const poll = () => {
            if (img.naturalWidth > 0) {stopped = true; clearTimeout(deadline); resolve();}
            else if (!stopped) setTimeout(poll, 50);
          };
          poll();
        }));
        try {
          await waitImage();
        } catch (error) {
          // Reload the actual image once when a deferred fetch stalls.
          // HTTP failures remain captured and cannot be masked by this retry.
          row.imageReloads.push(await img.getAttribute('src'));
          await img.evaluate(img => {img.src = img.src;});
          await waitImage();
        }
      }
      await page.evaluate(() => scrollTo(0, 0));
      await page.evaluate(async () => {
        await document.fonts.ready;
        await new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)));
      });
      // OINK initializes scrolling regions and the off-canvas drawer after
      // load. Assert the settled layout; persistent overflow still fails.
      await page.waitForFunction(() => document.documentElement.scrollWidth <= innerWidth + 1,
                                 undefined, {timeout:2000});
      const info = await page.evaluate(() => ({
        title:document.querySelector('.td-content h1').textContent,
        language:document.documentElement.lang,
        canonical:document.querySelector('link[rel=canonical]')?.href,
        width:document.documentElement.scrollWidth, viewport:innerWidth,
        sidebar:[...document.querySelectorAll('#td-section-nav .td-shell-tree__link')].map(a => new URL(a.href).pathname),
        pager:[...document.querySelectorAll('.td-pager a')].map(a => new URL(a.href).pathname),
        broken:[...document.querySelectorAll('.td-content img')].filter(i => !i.naturalWidth).map(i => i.currentSrc || i.dataset.src || i.src),
        tableCount:document.querySelectorAll('.td-content table').length,
      }));
      assert.equal(info.language, htmlLanguage, route);
      assert.equal(info.canonical, 'https://doc.pg.center' + route, route);
      assert(info.width <= info.viewport + 1, 'page overflow ' + route);
      assert.deepEqual(info.sidebar, routes, 'sidebar ' + route);
      assert.deepEqual(info.pager, [routes[index - 1], routes[index + 1]].filter(Boolean), 'pager ' + route);
      assert.deepEqual(info.broken, [], 'broken images ' + route);
      row.pages.push({route, title:info.title, tableCount:info.tableCount, overflow:info.width - info.viewport});
      if (route.endsWith('/etcd/') || route.endsWith('/dev-guide/api_reference_v3/') || route.endsWith('/op-guide/recovery/')) {
        await page.evaluate(() => document.fonts.ready);
        await page.screenshot({path:output + '/' + viewport.width + '-' + language + '-' + route.split('/').filter(Boolean).at(-1) + '.png'});
      }
    }
    const home = prefix + '/docs/etcd/';
    // The drawer and search bind separate deferred handlers. Exercise them
    // after the loaded page has initialized both controls.
    await page.goto(base + home, {waitUntil:'load'});
    if (viewport.width < 768) {
      await visible(page, '[data-td-shell-drawer-open]', 'click');
      await page.waitForFunction(() => document.documentElement.getAttribute('data-td-shell-drawer') === 'open');
      await visible(page, 'button[data-td-shell-drawer-close]', 'click');
      await page.waitForFunction(() => !document.documentElement.hasAttribute('data-td-shell-drawer'));
      row.interactions.push('mobile drawer open/close');
    }
    await visible(page, '[data-td-shell-search-open]', 'click');
    await page.locator('.td-shell-search__input').waitFor({state:'visible'});
    await page.locator('.td-shell-search__input').fill('etcdctl');
    const interaction = flatten(nav.root).find(n => n.id === '/docs/etcd/dev-guide/interacting_v3/');
    const result = page.locator('.td-shell-search__item').filter({
      has:page.locator('.td-shell-search__item-title').filter({hasText:interaction.title}),
    }).first();
    await result.waitFor({state:'visible', timeout:30000});
    await result.click();
    await page.waitForURL(u => u.pathname === home + 'dev-guide/interacting_v3/');
    row.interactions.push('technical search etcdctl -> interaction guide');
    await page.goto(base + home + 'learning/api/#range', {waitUntil:'domcontentloaded'});
    const anchor = await page.locator('#range').boundingBox();
    assert(anchor && anchor.y >= 0 && anchor.y < viewport.height, 'fragment jump ' + language);
    row.interactions.push('English #range fragment');
    if (language !== 'en') {
      await visible(page, '.td-language-selector__trigger', 'hover');
      await visible(page, '.td-language-selector__item[hreflang="en-US"]', 'click');
      await page.waitForURL(u => u.pathname === '/docs/etcd/learning/api/');
      await visible(page, '.td-language-selector__trigger', 'hover');
      await visible(page, '.td-language-selector__item[hreflang="' + htmlLanguage + '"]', 'click');
      await page.waitForURL(u => u.pathname === home + 'learning/api/');
      row.interactions.push('same-page language round trip');
    }
    assert.deepEqual(row.errors, [], 'browser runtime/HTTP errors ' + language);
    console.log(viewport.width, language, ':', row.pages.length, 'pages and interactions passed');
  } catch (e) {
    row.errors.push(e.stack);
    report.errors.push(language + ' ' + viewport.width + ': ' + e.message);
  } finally {
    await context.close();
  }
}
(async () => {
  const browser = await chromium.launch({headless:true, executablePath:process.env.CHROME_EXECUTABLE || undefined});
  try {
    for (const viewport of [{width:1440,height:1000}, {width:390,height:844}]) {
      // Two locales at a time bounds animated-image decoding and memory use.
    const selected = (process.env.ETCD_BROWSER_LANGUAGES || '').split(',').filter(Boolean);
    const entries = Object.entries(languages).filter(([lang]) => !selected.length || selected.includes(lang));
      for (let i = 0; i < entries.length; i += 2) {
        await Promise.all(entries.slice(i, i + 2).map(([lang, locale]) => checkLocale(browser, lang, locale, viewport)));
      }
    }
    report.status = report.errors.length ? 'failed' : 'passed';
  } finally {
    fs.writeFileSync(output + '/report.json', JSON.stringify(report, null, 2));
    await browser.close();
  }
  console.log(report.status, report.views.reduce((n, v) => n + v.pages.length, 0), 'page views;', report.errors.length, 'errors');
  if (report.errors.length) {console.error(report.errors.join('\n')); process.exitCode = 1;}
})().catch(e => {console.error(e); process.exitCode = 1;});
