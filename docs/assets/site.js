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
var th=d.getElementById('thBtn');if(th)th.addEventListener('click',function(){var n=h.getAttribute('data-theme')==='paper'?'night':'paper';h.setAttribute('data-theme',n);s('prophets.theme',n)});
// progress
var pr=d.querySelector('.prog'),tick=false;
function onS(){if(tick)return;tick=true;requestAnimationFrame(function(){var m=h.scrollHeight-h.clientHeight;pr.style.transform='scaleX('+(m>0?h.scrollTop/m:0)+')';tick=false})}
if(pr){window.addEventListener('scroll',onS,{passive:true});onS()}
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
// maps
d.querySelectorAll('.gmap').forEach(function(m){var inn=m.querySelector('.gm-in'),z=1,hs=m.querySelectorAll('.hs'),li=m.querySelectorAll('.gm-leg li');
 m.querySelectorAll('.gm-z button').forEach(function(b){b.addEventListener('click',function(){var k=+b.getAttribute('data-z');z=k===0?1:Math.max(1,Math.min(3,z+k*.5));inn.style.width=(z*100)+'%'})});
 function on(i,scroll){hs.forEach(function(x,j){x.classList.toggle('on',j==i)});li.forEach(function(x,j){x.classList.toggle('on',j==i)});
  if(scroll==='map'&&hs[i]){var v=m.querySelector('.gm-view'),r=hs[i];v.scrollTo({left:r.offsetLeft-v.clientWidth/2,top:r.offsetTop-v.clientHeight/2,behavior:'smooth'})}
  if(scroll==='leg'&&li[i]&&li[i].scrollIntoView){var p=li[i].parentElement;if(p.scrollHeight>p.clientHeight)p.scrollTop=li[i].offsetTop-p.offsetTop-40}}
 hs.forEach(function(b){b.addEventListener('click',function(){on(b.getAttribute('data-i'),'leg')})});
 li.forEach(function(x){function f(){on(x.getAttribute('data-i'),'map')}x.addEventListener('click',f);x.addEventListener('keydown',function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();f()}})})});
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
})();
