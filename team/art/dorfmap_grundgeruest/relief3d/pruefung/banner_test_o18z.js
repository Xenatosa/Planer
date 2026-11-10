// t118u: Handy-Hochformat-Test Banner vs Knoepfe. NODE_PATH=/tmp/w3/node_modules HTML=x.html OUT=png node pruefung/banner_test_o18z.js
const E=process.env,{chromium}=require('playwright'),path=require('path');
(async()=>{const b=await chromium.launch({args:['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist']});
const p=await b.newPage({viewport:{width:473,height:900},isMobile:true,hasTouch:true,deviceScaleFactor:1});
await p.goto('file://'+path.resolve(E.HTML));await p.waitForTimeout(+(E.WAIT||60000));
const pruef=()=>p.evaluate(()=>{const r=[];for(const el of document.querySelectorAll('button,#ban,#lab,input,select,label,a')){const q=el.getBoundingClientRect();if(!q.width||getComputedStyle(el).visibility=='hidden')continue;const x=q.left+q.width/2,y=q.top+q.height/2,h=document.elementFromPoint(x,y);const ban=document.getElementById('o18z_banner');r.push({el:(el.id||el.textContent||'').trim().slice(0,30),y:Math.round(q.top),frei:!(ban&&ban.contains(h))});}const k=document.getElementById('o18z_banner').getBoundingClientRect();return {banner:[Math.round(k.top),Math.round(k.bottom)],r};});
await p.screenshot({path:E.OUT+'_zu.png',timeout:600000});const a=await pruef();
await p.click('#o18z_kopf',{timeout:600000});await p.waitForTimeout(500);await p.screenshot({path:E.OUT+'_auf.png',timeout:600000});const c=await pruef();
console.log(JSON.stringify({zu:a,auf:{banner:c.banner,verdeckt:c.r.filter(x=>!x.frei)}}));await b.close();})();
