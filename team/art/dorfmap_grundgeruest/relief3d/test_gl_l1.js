// O10 L1: echte GPU-Dreiecke je Frame per WebGL-Hook (alle Durchgaenge), lod=1 Handy-Viewport
const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch({args:['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist']});
const p=await b.newPage({viewport:{width:390,height:844}});
await p.addInitScript(()=>{const L=window.__gl={calls:[],on:false};for(const C of [WebGL2RenderingContext,WebGLRenderingContext]){const P=C.prototype;
for(const f of ['drawElements','drawArrays','drawElementsInstanced','drawArraysInstanced']){const o=P[f];if(!o)continue;P[f]=function(...a){if(L.on){const fb=this.getParameter(this.FRAMEBUFFER_BINDING);const n=f.startsWith('drawArrays')?a[2]:a[1];const inst=f.endsWith('Instanced')?a[f=='drawArraysInstanced'?3:4]:1;L.calls.push([fb?1:0,n/3*inst,n/3,inst])}return o.apply(this,a)}}}});
await p.goto(process.argv[2]);await p.waitForFunction(()=>window.__test&&window.__test.bereit,null,{timeout:300000});await p.evaluate(()=>{__test.setModus('neu');__test.setView('schraeg')});await p.waitForTimeout(3000);
const r=await p.evaluate(()=>new Promise(res=>{requestAnimationFrame(()=>{__gl.calls=[];__gl.on=true;requestAnimationFrame(()=>{__gl.on=false;res(__gl.calls)})})}));
const s={fbo:0,bild:0};for(const c of r)s[c[0]?'fbo':'bild']+=c[1];r.sort((a,b)=>b[1]-a[1]);console.log(JSON.stringify({summe:s,n:r.length,top:r.slice(0,30)}));await b.close();})();
