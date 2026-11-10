// Handy-Bedienung: Touch-Emulation (hasTouch, 390x844), Tap auf Clay/Umriss/Wege/Start, Kamera vor/nach Ein-Finger-Wisch (CDP touch). Aufruf: node feld/test_bedienung.js feld.html out_prefix
const {chromium}=require('playwright');
(async()=>{const [f,out]=process.argv.slice(2);const b=await chromium.launch({args:['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist']});
const c=await b.newContext({viewport:{width:390,height:844},hasTouch:true,isMobile:true,deviceScaleFactor:1});const p=await c.newPage();const err=[];p.on('pageerror',e=>err.push(String(e)));
await p.goto('file://'+f);await p.waitForFunction(()=>window.__test&&window.__test.bereit&&window.__feld,null,{timeout:300000});await p.waitForTimeout(1500);
const kam=()=>p.evaluate(()=>{const s=window.__sc;let k=null;return window.__test.kamPos?window.__test.kamPos():null});
const um=()=>p.evaluate(()=>window.__sc.getObjectByName('feld_umriss').visible);
const cp=async()=>require('crypto').createHash('md5').update(await p.screenshot()).digest('hex').slice(0,8);const R={};R.btn=await p.evaluate(()=>['bclay','bum','bweg','bstart'].map(i=>{const r=document.getElementById(i).getBoundingClientRect();return [i,Math.round(r.width),Math.round(r.height)]}));
R.um0=await um();await p.tap('#bum');R.um1=await um();await p.tap('#bum');R.um2=await um();
R.clay0=await cp();await p.tap('#bclay');await p.waitForTimeout(800);R.clay1=await cp();await p.screenshot({path:out+'_clay.png'});await p.tap('#bclay');
R.weg0=await cp();await p.tap('#bweg');await p.waitForTimeout(500);R.weg1=await cp();await p.screenshot({path:out+'_ohnewege.png'});await p.tap('#bweg');
const cdp=await c.newCDPSession(p);const pos=()=>p.evaluate(()=>{const o=window.__oc||null;return JSON.stringify(window.__test.dump?null:null)});

R.cam0=await cp();const T=async(type,pts)=>cdp.send('Input.dispatchTouchEvent',{type,touchPoints:pts});
await T('touchStart',[{x:200,y:400}]);for(let i=1;i<=10;i++)await T('touchMove',[{x:200+i*12,y:400}]);await T('touchEnd',[]);await p.waitForTimeout(500);R.cam_dreh=await cp();
await T('touchStart',[{x:150,y:400,id:0},{x:250,y:400,id:1}]);for(let i=1;i<=10;i++)await T('touchMove',[{x:150-i*8,y:400,id:0},{x:250+i*8,y:400,id:1}]);await T('touchEnd',[]);await p.waitForTimeout(500);R.cam_zoom=await cp();
await p.screenshot({path:out+'_touch.png'});R.err=err;console.log(JSON.stringify(R));await b.close();})();
