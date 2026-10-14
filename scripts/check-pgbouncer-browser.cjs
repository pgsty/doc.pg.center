#!/usr/bin/env node
// Usage: PLAYWRIGHT_MODULE=/external/playwright CHROME_EXECUTABLE=/external/chrome
//        node scripts/check-pgbouncer-browser.cjs BASE_URL EXTERNAL_OUTPUT_DIR
const {chromium}=require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const fs=require('fs'); const assert=require('assert/strict');
const base=(process.argv[2]||'').replace(/\/$/,''); const output=process.argv[3]; assert(base&&output,'usage: BASE_URL EXTERNAL_OUTPUT_DIR'); fs.mkdirSync(output,{recursive:true});
const languages={en:'en-US',zh:'zh-CN',fr:'fr-FR',ja:'ja-JP',de:'de-DE',ru:'ru-RU'};
const slugs=['','features','config','usage','install','download','changelog','community','faq'];
const report={status:'running',viewports:[],errors:[]};
async function clickVisible(page,selector){const a=page.locator(selector);for(let i=0;i<await a.count();i++)if(await a.nth(i).isVisible()){await a.nth(i).click();return;}throw new Error('No visible '+selector);}
async function hoverVisible(page,selector){const a=page.locator(selector);for(let i=0;i<await a.count();i++)if(await a.nth(i).isVisible()){await a.nth(i).hover();return;}throw new Error('No visible '+selector);}
(async()=>{const browser=await chromium.launch({headless:true,executablePath:process.env.CHROME_EXECUTABLE || undefined});try{
for(const viewport of [{width:1440,height:1000},{width:390,height:844}]){
 const context=await browser.newContext({viewport,reducedMotion:'reduce'});const page=await context.newPage();const row={viewport,pages:[],search:[],errors:[]};report.viewports.push(row);
 await page.route(/https:\/\/(?:giscus\.app|(?:www\.)?google-analytics\.com|www\.googletagmanager\.com)\//,r=>r.fulfill({status:204,body:''}));
 page.on('pageerror',e=>row.errors.push(String(e)));page.on('response',r=>{if(r.status()>=400&&r.url().startsWith(base))row.errors.push(r.status()+' '+r.url());});
 for(const [language,locale] of Object.entries(languages)){
  const prefix=(language==='en'?'':'/'+language)+'/docs/pgbouncer/';const routes=slugs.map(s=>prefix+(s?s+'/':''));let configTitle='';
  for(const [index,route] of routes.entries()){
   await page.goto(base+route,{waitUntil:'domcontentloaded'});await page.locator('.td-content h1').waitFor({state:'visible'});
   const info=await page.evaluate(()=>({title:document.querySelector('.td-content h1').textContent,language:document.documentElement.lang,canonical:document.querySelector('link[rel=canonical]')?.href,width:document.documentElement.scrollWidth,viewport:innerWidth,characters:document.querySelector('.td-content').textContent.length,sidebar:[...document.querySelectorAll('#td-section-nav .td-shell-tree__link')].map(x=>new URL(x.href).pathname),pager:[...document.querySelectorAll('.td-pager a')].map(x=>new URL(x.href).pathname),broken:[...document.images].filter(x=>x.complete&&!x.naturalWidth).map(x=>x.src)}));
   assert.equal(info.language,locale,route);assert.equal(info.canonical,'https://doc.pg.center'+route,route);assert(info.width<=info.viewport+1,'overflow '+route);assert(info.characters>100,'empty '+route);assert.deepEqual(info.broken,[],route);assert.deepEqual(info.sidebar,routes,'sidebar '+route);assert.deepEqual(info.pager,[routes[index-1],routes[index+1]].filter(Boolean),'pager '+route);
   if(index===0)assert(info.title.includes('1.26.0'),route);if(route.endsWith('/config/'))configTitle=info.title;
   row.pages.push({route,...info});
   if(index===0||route.endsWith('/config/')){
    await page.evaluate(()=>document.fonts.ready);await page.screenshot({path:output+'/'+viewport.width+'-'+language+'-'+(index===0?'index':'config')+'.png'});
    if(viewport.width<768){await clickVisible(page,'[data-td-shell-drawer-open]');await page.waitForFunction(()=>document.documentElement.getAttribute('data-td-shell-drawer')==='open');await clickVisible(page,'button[data-td-shell-drawer-close]');await page.waitForFunction(()=>!document.documentElement.hasAttribute('data-td-shell-drawer'));}
   }
  }
  await page.goto(base+prefix,{waitUntil:'domcontentloaded'});await clickVisible(page,'[data-td-shell-search-open]');await page.locator('.td-shell-search__input').fill('pool_idle_timeout');
  const result=page.locator('.td-shell-search__item').filter({has:page.locator('.td-shell-search__item-title').filter({hasText:configTitle})}).first();await result.waitFor({state:'visible',timeout:10000});await result.click();await page.waitForURL(u=>u.pathname===prefix+'config/');row.search.push({language,query:'pool_idle_timeout',result:prefix+'config/'});
  if(language!=='en'){
   await hoverVisible(page,'.td-language-selector__trigger');await clickVisible(page,'.td-language-selector__item[hreflang="en-US"]');await page.waitForURL(u=>u.pathname==='/docs/pgbouncer/config/');await hoverVisible(page,'.td-language-selector__trigger');await clickVisible(page,'.td-language-selector__item[hreflang="'+locale+'"]');await page.waitForURL(u=>u.pathname===prefix+'config/');
  }
  console.log(viewport.width,language,': 9 pages and search/language controls passed');
 }
 assert.deepEqual(row.errors,[]);await context.close();
}
report.status='passed';}catch(e){report.status='failed';report.errors.push(e.stack);throw e;}finally{fs.writeFileSync(output+'/report.json',JSON.stringify(report,null,2));await browser.close();}})().catch(e=>{console.error(e);process.exit(1);});
