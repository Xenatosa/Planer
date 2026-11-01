const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const b=await chromium.launch({args:['--use-angle=swiftshader','--enable-unsafe-swiftshader']});const p=await b.newPage();
p.goto('file:///tmp/dl/o7.html',{timeout:0}).catch(()=>{});await p.waitForFunction(()=>window.__test&&window.__test.bereit,null,{timeout:150000,polling:1000});
const u=await p.evaluate(()=>{const {GX,GY,RS,WE,dist}=window.__wdbg,h=window.__hSurf;const x0=243,z0=258,S=26,px=0.1,N=S/px;const c=document.createElement('canvas');c.width=2*N+10;c.height=N;const g=c.getContext('2d'),im=g.createImageData(c.width,N);
const bil=(x,z,f)=>{const fi=x*RS,fj=z*RS,i=fi|0,j=fj|0,a=fi-i,bb=fj-j,k=j*GX+i;return f(k)*(1-a)*(1-bb)+f(k+1)*a*(1-bb)+f(k+GX)*(1-a)*bb+f(k+GX+1)*a*bb};
for(let y=0;y<N;y++)for(let x=0;x<N;x++){const X=x0+x*px,Z=z0+y*px,hb=h(X,Z);
 const fi=Math.round(X*RS),fj=Math.round(Z*RS),k=fj*GX+fi;const dOld=dist[k]==0?WE[k]-hb:NaN; const dNew=bil(X,Z,k=>WE[k])-hb;
 for(const[off,d]of[[0,dOld],[N+10,dNew]]){const o=(y*c.width+x+off)*4;let r,gg,bl;if(isNaN(d)||d<-5){r=gg=bl=40}else if(Math.abs(d)<0.02){r=255;gg=255;bl=0}else if(d>0){const t=Math.min(1,d/0.5);r=0;gg=80*(1-t);bl=120+135*t}else{const t=Math.min(1,-d/0.5);r=120+135*t;gg=60;bl=0}im.data[o]=r;im.data[o+1]=gg;im.data[o+2]=bl;im.data[o+3]=255}}
g.putImageData(im,0,0);return c.toDataURL()});
fs.writeFileSync(process.argv[2],Buffer.from(u.split(',')[1],'base64'));await b.close();process.exit(0)})();
