(function(){
var d=document,h=d.documentElement,LS=window.localStorage;
function g(k){try{return LS.getItem(k)}catch(e){return null}}function s(k,v){try{LS.setItem(k,v)}catch(e){}}
var wide=function(){return window.matchMedia('(min-width:1100px)').matches};
// TOC toggle
var tb=d.getElementById('tocBtn');
if(tb)tb.addEventListener('click',function(){if(wide()){h.classList.toggle('toc-off');s('prophets.toc',h.classList.contains('toc-off')?'off':'on')}else h.classList.toggle('toc-open')});
var sc=d.querySelector('.scrim');if(sc)sc.addEventListener('click',function(){h.classList.remove('toc-open')});
d.querySelectorAll('.toc a').forEach(function(a){a.addEventListener('click',function(){if(!wide())h.classList.remove('toc-open')})});
d.querySelectorAll('.toc .tg').forEach(function(b){b.addEventListener('click',function(){var li=b.closest('li');li.classList.toggle('closed');b.setAttribute('aria-expanded',!li.classList.contains('closed'))})});
var ex=d.getElementById('tocAll');if(ex)ex.addEventListener('click',function(){var c=d.querySelectorAll('.toc li.closed').length;d.querySelectorAll('.toc li.has').forEach(function(li){li.classList.toggle('closed',!c)})});
// TOC filter
var ti=d.getElementById('tocQ');if(ti)ti.addEventListener('input',function(){var q=ti.value.trim();d.querySelectorAll('.toc li').forEach(function(li){var t=li.textContent;li.style.display=!q||t.indexOf(q)>=0?'':'none';if(q)li.classList.remove('closed')})});
// theme
var th=d.getElementById('thBtn');if(th)th.addEventListener('click',function(){var n=h.getAttribute('data-theme')==='paper'?'night':'paper';h.classList.add('notr');h.setAttribute('data-theme',n);s('prophets.theme',n);var mt=d.querySelector('meta[name=theme-color]');if(mt)mt.content=n==='paper'?'#f7f1e4':'#0c1024';requestAnimationFrame(function(){requestAnimationFrame(function(){h.classList.remove('notr')})})});
// progress
var pr=d.querySelector('.prog'),tick=false;
function onS(){if(tick)return;tick=true;requestAnimationFrame(function(){var m=h.scrollHeight-h.clientHeight;pr.style.transform='scaleX('+(m>0?h.scrollTop/m:0)+')';tick=false})}
if(pr){window.addEventListener('scroll',onS,{passive:true});onS()}
var sT=0,sOn=false;window.addEventListener('scroll',function(){if(!sOn){sOn=true;h.classList.add('scrolling')}clearTimeout(sT);sT=setTimeout(function(){sOn=false;h.classList.remove('scrolling')},220)},{passive:true});
// scrollspy
var links={};d.querySelectorAll('.toc a[href^="#"]').forEach(function(a){links[a.getAttribute('href').slice(1)]=a});
if('IntersectionObserver' in window){
 var cur=null,io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){var a=links[e.target.id];if(a&&a!==cur){if(cur)cur.classList.remove('on');a.classList.add('on');cur=a;var li=a.closest('li.has');if(li)li.classList.remove('closed');if(a.scrollIntoViewIfNeeded)a.scrollIntoViewIfNeeded(false)}}})},{rootMargin:'-70px 0px -70% 0px'});
 d.querySelectorAll('main h2[id],main h3[id]').forEach(function(x){io.observe(x)});
 if(!window.matchMedia('(prefers-reduced-motion:reduce)').matches){
  var ro=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');ro.unobserve(e.target)}})},{rootMargin:'0px 0px -8% 0px'});
  d.querySelectorAll('.reveal').forEach(function(x){ro.observe(x)});
 } else d.querySelectorAll('.reveal').forEach(function(x){x.classList.add('in')});
} else d.querySelectorAll('.reveal').forEach(function(x){x.classList.add('in')});
// story stepper
d.querySelectorAll('.story').forEach(function(st){var ss=st.querySelectorAll('.st'),ds=st.querySelectorAll('.dot'),i=0,tm=null;
 function go(n){i=(n+ss.length)%ss.length;ss.forEach(function(x,j){x.classList.toggle('on',j===i)});ds.forEach(function(x,j){x.classList.toggle('on',j===i)})}
 ds.forEach(function(b,j){b.addEventListener('click',function(){stop();go(j)})});
 var pv=st.querySelector('[data-a=p]'),nx=st.querySelector('[data-a=n]'),pl=st.querySelector('[data-a=play]');
 function stop(){if(tm){clearInterval(tm);tm=null;if(pl)pl.textContent='▶ 自动播放'}}
 if(pv)pv.addEventListener('click',function(){stop();go(i-1)});if(nx)nx.addEventListener('click',function(){stop();go(i+1)});
 if(pl)pl.addEventListener('click',function(){if(tm){stop();return}pl.textContent='⏸ 暂停';tm=setInterval(function(){go(i+1)},4200)});go(0)});
// flip cards
d.querySelectorAll('.flip').forEach(function(f){f.setAttribute('tabindex','0');function t(){f.classList.toggle('on')}f.addEventListener('click',t);f.addEventListener('keydown',function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();t()}})});
var fa=d.getElementById('flipAll');if(fa)fa.addEventListener('click',function(){var fs=d.querySelectorAll('.flip'),any=d.querySelectorAll('.flip.on').length;fs.forEach(function(f){f.classList.toggle('on',!any)})});
// quiz
d.querySelectorAll('.quiz').forEach(function(q){var tot=q.querySelectorAll('.qq').length,ok=0,sc=q.querySelector('.score');
 q.querySelectorAll('.qq').forEach(function(x){x.querySelectorAll('button.o').forEach(function(b){b.addEventListener('click',function(){if(x.classList.contains('done'))return;x.classList.add('done');
  if(b.hasAttribute('data-ok')){b.classList.add('ok');ok++}else{b.classList.add('no');var r=x.querySelector('[data-ok]');if(r)r.classList.add('ok')}
  if(sc)sc.textContent='得分 '+ok+' / '+tot})})});
 var rs=q.querySelector('[data-a=reset]');if(rs)rs.addEventListener('click',function(){ok=0;q.querySelectorAll('.qq').forEach(function(x){x.classList.remove('done');x.querySelectorAll('.o').forEach(function(b){b.classList.remove('ok','no')})});if(sc)sc.textContent='得分 0 / '+tot})});
// recite mode
d.querySelectorAll('[data-recite]').forEach(function(b){var c=d.getElementById(b.getAttribute('data-recite'));b.addEventListener('click',function(){c.classList.toggle('recite');c.querySelectorAll('.ln').forEach(function(l){l.classList.remove('show')});b.textContent=c.classList.contains('recite')?'👁️ 显示全文':'🙈 背诵模式（遮盖）'})});
d.querySelectorAll('.creed').forEach(function(c){c.addEventListener('click',function(e){var l=e.target.closest('.ln');if(l&&c.classList.contains('recite'))l.classList.toggle('show')})});
d.querySelectorAll('[data-big]').forEach(function(b){var c=d.getElementById(b.getAttribute('data-big'));b.addEventListener('click',function(){var f=parseFloat(getComputedStyle(c).fontSize);c.style.fontSize=(f*(b.getAttribute('data-d')==='+'?1.1:0.9))+'px'})});
var top=d.getElementById('toTop');if(top)top.addEventListener('click',function(){window.scrollTo({top:0,behavior:'smooth'})});
// ===== v2 =====
var RM=window.matchMedia('(prefers-reduced-motion:reduce)').matches,V=(d.currentScript&&d.currentScript.src.split('?v=')[1])||'';
// 图片断网重试一次
d.querySelectorAll('img').forEach(function(im){im.addEventListener('error',function(){if(im.dataset.retry)return;im.dataset.retry=1;setTimeout(function(){im.src=im.src.split('&r=')[0]+(im.src.indexOf('?')>0?'&':'?')+'r='+Date.now()},1500)})});
// 地图：讲解图 / 地形图 / 实时地图
var lmLoading=null;function loadLM(){if(window.ProphetsLiveMap)return Promise.resolve();if(lmLoading)return lmLoading;lmLoading=new Promise(function(res,rej){var s=d.createElement('script');s.src='assets/livemap.js?v='+V;s.onload=res;s.onerror=function(){lmLoading=null;rej()};d.head.appendChild(s)});return lmLoading}
d.querySelectorAll('.gmap').forEach(function(m){var z=1,li=m.querySelectorAll('.gm-leg li'),tabs=m.querySelectorAll('.mx-tabs [role=tab]'),panes=m.querySelectorAll('.mx-pane'),cur='c';
 function act(){return m.querySelector('.mx-pane.on')||m}
 function sw(p){cur=p;tabs.forEach(function(t){t.setAttribute('aria-selected',t.getAttribute('data-p')===p)});panes.forEach(function(x){x.classList.toggle('on',x.getAttribute('data-p')===p)});m.setAttribute('data-p',p);
  var pn=act();pn.querySelectorAll('img[data-src]').forEach(function(im){im.src=im.getAttribute('data-src');im.removeAttribute('data-src')});
  if(p==='l'){var st=pn.querySelector('.lm-st');if(st)st.textContent='⏳ 正在载入地图引擎…';loadLM().then(function(){var a=window.ProphetsLiveMap.init(m);if(a.dead)a.retry();a.resize()},function(){if(st)st.textContent='⚠️ 地图脚本加载失败，已切回本地讲解图';sw('c')})}}
 m._switch=sw;tabs.forEach(function(t){t.addEventListener('click',function(){sw(t.getAttribute('data-p'))})});
 m.querySelectorAll('.gm-z button').forEach(function(b){b.addEventListener('click',function(){var k=+b.getAttribute('data-z');z=k===0?1:Math.max(1,Math.min(3,z+k*.5));
  if(cur==='l'&&m._lm&&m._lm.map){k===0?m._lm.map.fitBounds([[JSON.parse(m.getAttribute('data-map')).b[2],JSON.parse(m.getAttribute('data-map')).b[0]],[JSON.parse(m.getAttribute('data-map')).b[3],JSON.parse(m.getAttribute('data-map')).b[1]]]):m._lm.map.setZoom(m._lm.map.getZoom()+k);return}
  m.querySelectorAll('.gm-in').forEach(function(inn){inn.style.width=(z*100)+'%'})})});
 function on(i,scroll){var hs=m.querySelectorAll('.hs');hs.forEach(function(x,j){x.classList.toggle('on',j==i)});li.forEach(function(x,j){x.classList.toggle('on',j==i)});
  if(cur==='l'&&m._lm){m._lm.fly(+i);return}
  if(scroll==='map'&&cur==='t'&&hs[i]){var v=act().querySelector('.gm-view'),r=hs[i];v.scrollTo({left:r.offsetLeft-v.clientWidth/2,top:r.offsetTop-v.clientHeight/2,behavior:RM?'auto':'smooth'})}
  if(scroll==='leg'&&li[i]){var p=li[i].parentElement;if(p.scrollHeight>p.clientHeight)p.scrollTop=li[i].offsetTop-p.offsetTop-40}}
 m.addEventListener('click',function(e){var b=e.target.closest('.hs');if(b)on(b.getAttribute('data-i'),'leg')});
 li.forEach(function(x){function f(){on(x.getAttribute('data-i'),'map')}x.addEventListener('click',f);x.addEventListener('keydown',function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();f()}})})});
// 视频：点击才加载（YouTube 无 Cookie 域名；备用 MP4 直链）
d.querySelectorAll('.vid').forEach(function(v){var box=v.querySelector('.vbox');
 function put(html){box.innerHTML=html;v.classList.add('playing')}
 v.querySelector('[data-a=yt]').addEventListener('click',function(){put('<iframe src="https://www.youtube-nocookie.com/embed/'+v.getAttribute('data-yt')+'?autoplay=1&rel=0&cc_lang_pref=zh-Hans" title="'+(v.getAttribute('data-t')||'视频')+'" allow="autoplay; encrypted-media; picture-in-picture; fullscreen" allowfullscreen loading="lazy"></iframe>')});
 var mp=v.querySelector('[data-a=mp4]');if(mp)mp.addEventListener('click',function(){put('<video controls autoplay playsinline preload="metadata" src="'+v.getAttribute('data-mp4')+'"></video>')})});
// 标记系统：图例开关、彩色/简洁、遮盖重点（背诵）
function setMode(k,on){h.classList.toggle(k,on);s('prophets.'+k,on?'1':'0');d.querySelectorAll('[data-mode="'+k+'"]').forEach(function(b){b.setAttribute('aria-pressed',on)})}
['plain','cloze'].forEach(function(k){if(g('prophets.'+k)==='1')setMode(k,true)});
d.querySelectorAll('[data-mode]').forEach(function(b){b.addEventListener('click',function(){var k=b.getAttribute('data-mode');setMode(k,!h.classList.contains(k));if(k==='cloze')d.querySelectorAll('.k.show,.cv.show,.xr.show').forEach(function(x){x.classList.remove('show')})})});
d.addEventListener('click',function(e){if(!h.classList.contains('cloze'))return;var t=e.target.closest('main .k,main .xr,main .cv');if(t&&!t.closest('a,button')){t.classList.toggle('show')}});
// 预取：悬停/触摸站内链接时预取下一页（不支持 Speculation Rules 的浏览器）
if(!(HTMLScriptElement.supports&&HTMLScriptElement.supports('speculationrules'))){var pf={};function pre(a){var u=a.getAttribute('href');if(!u||pf[u]||/^(https?:|#|mailto:)/.test(u))return;pf[u]=1;var l=d.createElement('link');l.rel='prefetch';l.href=u;d.head.appendChild(l)}
 d.addEventListener('pointerover',function(e){var a=e.target.closest&&e.target.closest('a[href$=".html"]');if(a)pre(a)},{passive:true});d.addEventListener('touchstart',function(e){var a=e.target.closest&&e.target.closest('a[href$=".html"]');if(a)pre(a)},{passive:true})}
// 离线缓存（Service Worker：同源页面与资源）
if('serviceWorker' in navigator&&location.protocol.indexOf('http')===0){window.addEventListener('load',function(){navigator.serviceWorker.register('sw.js?v='+V).catch(function(){})})}
})();
