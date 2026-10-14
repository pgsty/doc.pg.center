#!/usr/bin/env node
// Usage: PLAYWRIGHT_MODULE=/external/playwright CHROME_EXECUTABLE=/external/chrome
//        node scripts/check-pgbadger-browser.cjs BASE_URL EXTERNAL_OUTPUT_DIR
const {chromium}=require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const fs=require('fs'); const assert=require('assert/strict');
const path=require('node:path');
const base=(process.argv[2]||'').replace(/\/$/,''); const requestedOutput=process.argv[3]; assert(base&&requestedOutput,'usage: BASE_URL EXTERNAL_OUTPUT_DIR');
// Resolve the nearest existing ancestor too, so a symlink cannot redirect
// screenshots or reports into the repository.
const absoluteOutput=path.resolve(requestedOutput);let ancestor=absoluteOutput;
while(!fs.existsSync(ancestor))ancestor=path.dirname(ancestor);
const output=path.resolve(fs.realpathSync(ancestor),path.relative(ancestor,absoluteOutput));
const project=fs.realpathSync(path.resolve(__dirname,'..'));
assert(output!==project&&!output.startsWith(project+path.sep),'generated browser evidence must be outside the source repository');
fs.mkdirSync(output,{recursive:true});
const languages={en:'en-US',zh:'zh-CN',fr:'fr-FR',ja:'ja-JP',de:'de-DE',ru:'ru-RU'};
const slugs=['','download','command-line','postgresql-logging','parallel-processing','incremental-reports','output-formats','sample-reports','releases','releases/13','releases/12','releases/11','releases/10','releases/9','support','license'];
const report={status:'running',viewports:[],errors:[]};
async function clickVisible(page,selector){const a=page.locator(selector);for(let i=0;i<await a.count();i++)if(await a.nth(i).isVisible()){await a.nth(i).click();return;}throw new Error('No visible '+selector);}
async function hoverVisible(page,selector){const a=page.locator(selector);for(let i=0;i<await a.count();i++)if(await a.nth(i).isVisible()){await a.nth(i).hover();return;}throw new Error('No visible '+selector);}
(async()=>{const browser=await chromium.launch({headless:true,executablePath:process.env.CHROME_EXECUTABLE || undefined});try{
for(const viewport of [{width:1440,height:1000},{width:390,height:844}]){
 const context=await browser.newContext({viewport,reducedMotion:'reduce'});const page=await context.newPage();const row={viewport,pages:[],search:[],errors:[],requestFailures:[]};report.viewports.push(row);
 // Block external comments/analytics through Chromium while preserving normal
 // HTTP caching; Playwright request routing disables the cache for every asset.
 const network=await context.newCDPSession(page);await network.send('Network.enable');
 await network.send('Network.setBlockedURLs',{urls:['https://giscus.app/*','https://google-analytics.com/*','https://www.google-analytics.com/*','https://www.googletagmanager.com/*']});
 page.on('pageerror',e=>row.errors.push(String(e)));page.on('response',r=>{if(r.status()>=400&&r.url().startsWith(base))row.errors.push(r.status()+' '+r.url());});
 page.on('requestfailed',r=>{const reason=r.failure()?.errorText||'';if(r.url().startsWith(base)&&reason!=='net::ERR_ABORTED')row.requestFailures.push({url:r.url(),reason});});
 for(const [language,locale] of Object.entries(languages)){
  const prefix=(language==='en'?'':'/'+language)+'/docs/pgbadger/';const routes=slugs.map(s=>prefix+(s?s+'/':''));let loggingTitle='',commandTitle='',incrementalTitle='';
  for(const [index,route] of routes.entries()){
   await page.goto(base+route,{waitUntil:'load'});await page.locator('.td-content h1').waitFor({state:'visible'});await page.waitForLoadState('load');await page.evaluate(async()=>{await document.fonts.ready;await Promise.all([...document.images].filter(x=>x.currentSrc).map(x=>x.decode().catch(()=>{})));});
   const info=await page.evaluate(()=>({title:document.querySelector('.td-content h1').textContent,language:document.documentElement.lang,canonical:document.querySelector('link[rel=canonical]')?.href,width:document.documentElement.scrollWidth,viewport:innerWidth,characters:document.querySelector('.td-content').textContent.length,sidebar:[...document.querySelectorAll('#td-section-nav .td-shell-tree__link')].map(x=>new URL(x.href).pathname),pager:[...document.querySelectorAll('.td-pager a')].map(x=>new URL(x.href).pathname),broken:[...document.images].filter(x=>x.currentSrc&&x.complete&&!x.naturalWidth).map(x=>x.src)}));
   assert.equal(info.language,locale,route);assert.equal(info.canonical,'https://doc.pg.center'+route,route);assert(info.width<=info.viewport+1,'overflow '+route);assert(info.characters>100,'empty '+route);assert.deepEqual(info.broken,[],route);assert.deepEqual(info.sidebar,routes,'sidebar '+route);assert.deepEqual(info.pager,[routes[index-1],routes[index+1]].filter(Boolean),'pager '+route);
   if(index===0)assert(info.title.includes('13.2'),route);if(route.endsWith('/postgresql-logging/'))loggingTitle=info.title;if(route.endsWith('/command-line/'))commandTitle=info.title;if(route.endsWith('/incremental-reports/'))incrementalTitle=info.title;
   row.pages.push({route,...info});
   if(index===0||route.endsWith('/postgresql-logging/')||route.endsWith('/command-line/')){
    await page.evaluate(()=>document.fonts.ready);await page.screenshot({path:output+'/'+viewport.width+'-'+language+'-'+(index===0?'index':route.endsWith('/command-line/')?'command-line':'logging')+'.png'});
    if(viewport.width<768){await clickVisible(page,'[data-td-shell-drawer-open]');await page.waitForFunction(()=>document.documentElement.getAttribute('data-td-shell-drawer')==='open');await clickVisible(page,'button[data-td-shell-drawer-close]');await page.waitForFunction(()=>!document.documentElement.hasAttribute('data-td-shell-drawer'));}
   }
  }
  for(const [query,title,slug] of [['--ssh-sudo',commandTitle,'command-line'],['--retention',incrementalTitle,'incremental-reports'],['log_min_duration_statement',loggingTitle,'postgresql-logging']]){
   await page.goto(base+prefix,{waitUntil:'load'});await clickVisible(page,'[data-td-shell-search-open]');await page.locator('.td-shell-search__input').fill(query);
   const result=page.locator('.td-shell-search__item').filter({has:page.locator('.td-shell-search__item-title').filter({hasText:title})}).first();await result.waitFor({state:'visible',timeout:10000});await result.click();await page.waitForURL(u=>u.pathname===prefix+slug+'/');await page.waitForLoadState('load');row.search.push({language,query,result:prefix+slug+'/'});
  }
  if(language!=='en'){
   await hoverVisible(page,'.td-language-selector__trigger');await clickVisible(page,'.td-language-selector__item[hreflang="en-US"]');await page.waitForURL(u=>u.pathname==='/docs/pgbadger/postgresql-logging/');await page.waitForLoadState('load');await hoverVisible(page,'.td-language-selector__trigger');await clickVisible(page,'.td-language-selector__item[hreflang="'+locale+'"]');await page.waitForURL(u=>u.pathname===prefix+'postgresql-logging/');await page.waitForLoadState('load');
  }
  console.log(viewport.width,language,': 16 pages and search/language controls passed');
 }
 assert.deepEqual(row.errors,[]);await context.close();
}
report.status='passed';}catch(e){report.status='failed';report.errors.push(e.stack);throw e;}finally{fs.writeFileSync(output+'/report.json',JSON.stringify(report,null,2));await browser.close();}})().catch(e=>{console.error(e);process.exit(1);});
