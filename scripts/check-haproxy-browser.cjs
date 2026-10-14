#!/usr/bin/env node
'use strict';

// Serve the production build locally before running this check. Playwright
// and its isolated Chromium runtime live outside the source repository.
// Usage: PLAYWRIGHT_MODULE=/path/to/playwright CHROME_EXECUTABLE=/path/to/chrome
//        HAPROXY_LANGUAGE=zh node scripts/check-haproxy-browser.cjs BASE_URL OUTPUT_DIR
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'playwright');

const base = (process.argv[2] || '').replace(/\/$/, '');
const output = process.argv[3];
const language = process.env.HAPROXY_LANGUAGE || 'ja';
const locales = {en:'en-US',zh:'zh-CN',fr:'fr-FR',ja:'ja-JP',de:'de-DE',ru:'ru-RU'};
assert(locales[language], 'unsupported language');
const localePrefix = language === 'en' ? '' : '/' + language;
const peer = language === 'en' ? 'zh' : 'en';
const peerPrefix = peer === 'en' ? '' : '/' + peer;
const peerLocale = locales[peer];
const expectedCount = 35;
assert(base && output, 'usage: BASE_URL OUTPUT_DIR');
fs.mkdirSync(output, { recursive: true });
const report = { base, language, expectedCount, viewports: [], errors: [], status: 'running' };
const prefix = localePrefix + '/docs/haproxy/';
const representative = new Set([
  prefix, prefix + 'acls-and-samples/', prefix + 'global/', prefix + 'proxies/',
  prefix + 'configuration-logging/', prefix + 'statistics-and-monitoring/',
  prefix + 'bind-and-server-options/',
]);
function* walk(node) {
  yield node;
  for (const child of node.children || []) yield* walk(child);
}
async function visibleClick(page, selector) {
  const all = page.locator(selector);
  for (let i = 0; i < await all.count(); i++) {
    if (await all.nth(i).isVisible()) { await all.nth(i).click(); return; }
  }
  throw new Error('No visible control: ' + selector);
}
async function visibleHover(page, selector) {
  const all = page.locator(selector);
  for (let i = 0; i < await all.count(); i++) {
    if (await all.nth(i).isVisible()) { await all.nth(i).hover(); return; }
  }
  throw new Error('No visible control: ' + selector);
}
async function run() {
  const browser = await chromium.launch({ headless: true, executablePath: process.env.CHROME_EXECUTABLE || undefined });
  try {
    for (const viewport of [{ width: 1440, height: 1000 }, { width: 390, height: 844 }]) {
      // Deterministic sequential jumps also exercise the site's reduced-motion
      // mode, without interrupting an in-progress smooth scroll with the next.
      const context = await browser.newContext({ viewport, reducedMotion: 'reduce' });
      const page = await context.newPage();
      const evidence = { viewport, reducedMotion: 'reduce', pages: [], search: [], consoleErrors: [], requestFailures: [], omittedThirdPartyRequests: [] };
      report.viewports.push(evidence);
      // Local acceptance does not contact the deployed analytics/comment
      // services. Record this explicit boundary; all site assets still load.
      await page.route(/https:\/\/(?:giscus\.app|(?:www\.)?google-analytics\.com|www\.googletagmanager\.com)\//, async (route) => {
        evidence.omittedThirdPartyRequests.push(route.request().url());
        await route.fulfill({ status: 204, body: '' });
      });
      page.on('pageerror', (error) => evidence.consoleErrors.push(String(error)));
      page.on('console', (message) => {
        if (message.type() === 'error') evidence.consoleErrors.push(message.text());
      });
      page.on('requestfailed', (request) => evidence.requestFailures.push({
        url: request.url(), error: request.failure()?.errorText,
      }));
      page.on('response', (response) => {
        if (response.status() >= 400) evidence.requestFailures.push({
          url: response.url(), status: response.status(),
        });
      });
      await page.goto(base + prefix, { waitUntil: 'networkidle' });
      const navigation = await (await context.request.get(base + localePrefix + '/navigation.json')).json();
      const nodes = [...walk(navigation.root)].filter((node) => node.id?.startsWith('/docs/haproxy/'));
      assert.equal(nodes.length, expectedCount, 'production navigation must contain the complete logical page set');
      const routes = nodes.map((node) => new URL(node.url).pathname);
      assert.equal(new Set(routes).size, expectedCount, 'duplicate production navigation routes');
      for (const [index, route] of routes.entries()) {
        const response = await page.goto(base + route, { waitUntil: 'networkidle' });
        assert.equal(response.status(), 200, route);
        await page.locator('.td-content h1').waitFor({ state: 'visible' });
        await page.evaluate(() => document.fonts.ready);
        const snapshot = await page.evaluate(({ localePrefix, peerPrefix }) => ({
          title: document.title,
          language: document.documentElement.lang,
          canonical: document.querySelector('link[rel=canonical]')?.href,
          sidebar: [...document.querySelectorAll('#td-section-nav .td-shell-tree__link')].map((el) => new URL(el.href).pathname),
          pager: [...document.querySelectorAll('.td-pager a')].map((el) => new URL(el.href).pathname),
          fallbacks: [...document.querySelectorAll('[data-fallback-language]')].map((el) => el.getAttribute('href')),
          englishSwitch: [...document.querySelectorAll('.td-language-selector__item')].some((el) => new URL(el.getAttribute('href') || location.href, location.href).pathname === peerPrefix + location.pathname.slice(localePrefix.length)),
          width: document.documentElement.scrollWidth,
          viewport: innerWidth,
          contentCharacters: document.querySelector('.td-content')?.textContent.length,
          anchors: [...document.querySelectorAll('.td-content h2[id], .td-content h3[id]')].map((el) => el.id),
          brokenImages: [...document.querySelectorAll('img')].filter((el) => el.complete && !el.naturalWidth).map((el) => el.src),
        }), { localePrefix, peerPrefix });
        assert.equal(snapshot.language, locales[language], route);
        assert(snapshot.title.length > 0, route);
        assert.equal(snapshot.canonical, 'https://doc.pg.center' + route, route);
        assert.deepEqual(snapshot.sidebar, routes, 'sidebar order: ' + route);
        const expectedPager = [routes[index - 1], routes[index + 1]].filter(Boolean);
        assert.deepEqual(snapshot.pager, expectedPager, 'adjacent pager routes: ' + route);
        assert(!snapshot.fallbacks.some((value) => value?.includes('/docs/haproxy/')), 'HAProxy fallback: ' + route);
        assert(snapshot.englishSwitch, 'English switch: ' + route);
        assert(snapshot.width <= snapshot.viewport + 1, 'document overflow: ' + route);
        assert(snapshot.contentCharacters > 100, 'empty content: ' + route);
        assert.deepEqual(snapshot.brokenImages, [], 'broken images: ' + route);
        if (representative.has(route)) {
          if (viewport.width < 768) {
            assert.equal(await page.locator('html').getAttribute('data-td-shell-drawer'), null);
            await visibleClick(page, '[data-td-shell-drawer-open]');
            await page.waitForFunction(() => document.documentElement.getAttribute('data-td-shell-drawer') === 'open');
            await visibleClick(page, 'button[data-td-shell-drawer-close]');
            await page.waitForFunction(() => !document.documentElement.hasAttribute('data-td-shell-drawer'));
          }
          await page.screenshot({ path: path.join(output, `${viewport.width}-${route.split('/').filter(Boolean).pop()}.png`) });
          // Open the actual menu and navigate to the same English page, then
          // use its language menu to return to Japanese at both widths.
          const englishRoute = peerPrefix + route.slice(localePrefix.length);
          await visibleHover(page, '.td-language-selector__trigger');
          await visibleClick(page, '.td-language-selector__item[hreflang="' + peerLocale + '"]');
          await page.waitForURL((url) => url.pathname === englishRoute, { waitUntil: 'networkidle' });
          assert.equal(await page.locator('html').getAttribute('lang'), peerLocale, route);
          await visibleHover(page, '.td-language-selector__trigger');
          await visibleClick(page, '.td-language-selector__item[hreflang="' + locales[language] + '"]');
          await page.waitForURL((url) => url.pathname === route, { waitUntil: 'networkidle' });
          assert.equal(await page.locator('html').getAttribute('lang'), locales[language], route);
          await page.evaluate(() => document.fonts.ready);
          snapshot.languageSwitchJourney = { english: englishRoute, localized: route };
          // Exercise both ends of a long page using its stable English IDs.
          const anchors = [...new Set([snapshot.anchors[0], snapshot.anchors.at(-1)])].filter(Boolean);
          for (const anchor of anchors) {
            // A same-document native hash jump avoids a full reload while
            // fonts are laying out the long page a second time.
            await page.evaluate((id) => { location.hash = id; }, anchor);
            await page.waitForFunction((id) => {
              const box = document.getElementById(id)?.getBoundingClientRect();
              return box && box.bottom > 0 && box.top < innerHeight;
            }, anchor);
          }
          snapshot.testedAnchors = anchors;
        }
        evidence.pages.push({ route, ...snapshot });
      }
      // Follow a real sidebar link and both pager directions at each width.
      await page.goto(base + prefix, { waitUntil: 'networkidle' });
      if (viewport.width < 768) await visibleClick(page, '[data-td-shell-drawer-open]');
      await page.locator('#td-section-nav .td-shell-tree__link[href="' + prefix + 'cache/"]').click();
      await page.waitForURL((url) => url.pathname === prefix + 'cache/', { waitUntil: 'networkidle' });
      await page.locator('[data-td-pager-next]').click();
      await page.waitForURL((url) => url.pathname === prefix + 'acls-and-samples/', { waitUntil: 'networkidle' });
      await page.locator('[data-td-pager-prev]').click();
      await page.waitForURL((url) => url.pathname === prefix + 'cache/', { waitUntil: 'networkidle' });
      evidence.navigationJourney = [prefix, prefix + 'cache/', prefix + 'acls-and-samples/', prefix + 'cache/'];
      // Test real interactive search, then activate a localized result.
      for (const [query, wanted] of [[{en:'Cache',zh:'缓存',fr:'Cache',ja:'キャッシュ',de:'Cache',ru:'Кеш'}[language], prefix + 'cache/'], [{en:'Statistics',zh:'统计',fr:'Statistiques',ja:'統計情報',de:'Statistik',ru:'Статистика'}[language], prefix + 'statistics-and-monitoring/'], ['HAProxy', prefix]]) {
        const target = nodes.find((node) => new URL(node.url).pathname === wanted);
        if (!target) continue;
        await page.goto(base + prefix, { waitUntil: 'networkidle' });
        await visibleClick(page, '[data-td-shell-search-open]');
        await page.locator('.td-shell-search__input').fill(query);
        const title = evidence.pages.find((entry) => entry.route === wanted).title.replace(/\s*\|.*$/, '');
        const exactTitle = new RegExp('^' + title.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + '$');
        const row = page.locator('.td-shell-search__item').filter({
          has: page.locator('.td-shell-search__item-title').filter({ hasText: exactTitle }),
        }).first();
        await row.waitFor({ state: 'visible' });
        const text = await row.innerText();
        await row.click();
        await page.waitForURL((url) => url.pathname === wanted, { waitUntil: 'domcontentloaded' });
        evidence.search.push({ query, route: wanted, resultText: text });
      }
      assert.deepEqual(evidence.consoleErrors, [], 'browser console errors');
      assert.deepEqual(evidence.requestFailures, [], 'browser request errors');
      await context.close();
      console.log(`Validated ${viewport.width}x${viewport.height}: ${evidence.pages.length} pages, sidebar, pager, language controls, anchors and interactive search.`);
    }
    report.status = 'passed';
  } finally {
    await browser.close();
  }
}
run().catch((error) => {
  report.status = 'failed';
  report.errors.push(String(error.stack || error));
  console.error(error);
  process.exitCode = 1;
}).finally(() => {
  fs.writeFileSync(path.join(output, 'browser-report.json'), JSON.stringify(report, null, 2) + '\n');
});
