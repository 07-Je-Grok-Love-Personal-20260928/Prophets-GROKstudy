/* 先知书 v2 · 实时地图：自托管 Leaflet（assets/vendor/leaflet），12 个全球底图源，瓦片出错自动换源，全部失败回到本地讲解图。 */
(function(){
var d=document,V=(d.currentScript&&d.currentScript.src.split('?v=')[1])||'';
var SRC=[
 {k:'carto',n:'CARTO Voyager（全球 CDN）',u:'https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png',s:'abcd',a:'© OpenStreetMap · © CARTO',mz:19},
 {k:'esritopo',n:'Esri 世界地形 Topo',u:'https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}',a:'© Esri',mz:19},
 {k:'gaode',n:'高德地图（中国大陆可用 · 中文）',u:'https://webrd0{s}.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=8&x={x}&y={y}&z={z}',s:'1234',a:'© 高德地图 AutoNavi',mz:18},
 {k:'osm',n:'OpenStreetMap 标准',u:'https://tile.openstreetmap.org/{z}/{x}/{y}.png',a:'© OpenStreetMap contributors',mz:19},
 {k:'esrisat',n:'Esri 卫星影像',u:'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',a:'© Esri, Maxar, Earthstar',mz:19},
 {k:'natgeo',n:'Esri 国家地理风格',u:'https://server.arcgisonline.com/ArcGIS/rest/services/NatGeo_World_Map/MapServer/tile/{z}/{y}/{x}',a:'© Esri, National Geographic',mz:16},
 {k:'phys',n:'Esri 自然地貌（古地理感）',u:'https://server.arcgisonline.com/ArcGIS/rest/services/World_Physical_Map/MapServer/tile/{z}/{y}/{x}',a:'© Esri, US NPS',mz:8},
 {k:'otm',n:'OpenTopoMap 等高线',u:'https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png',s:'abc',a:'© OpenStreetMap · SRTM · © OpenTopoMap',mz:17},
 {k:'hot',n:'OSM 人道主义 HOT',u:'https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png',s:'abc',a:'© OpenStreetMap · OSM France',mz:19},
 {k:'gaodesat',n:'高德卫星（中国大陆可用）',u:'https://webst0{s}.is.autonavi.com/appmaptile?style=6&x={x}&y={y}&z={z}',s:'1234',a:'© 高德地图 AutoNavi',mz:18},
 {k:'light',n:'CARTO 浅色',u:'https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png',s:'abcd',a:'© OpenStreetMap · © CARTO',mz:19},
 {k:'dark',n:'CARTO 深色',u:'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png',s:'abcd',a:'© OpenStreetMap · © CARTO',mz:19}];
function cn(){try{var z=Intl.DateTimeFormat().resolvedOptions().timeZone||'';return /Shanghai|Chongqing|Urumqi|Harbin/.test(z)}catch(e){return false}}
function pref(){try{return localStorage.getItem('prophets.tiles')}catch(e){return null}}
function setPref(k){try{localStorage.setItem('prophets.tiles',k)}catch(e){}}
var order=function(){var o=SRC.slice();if(cn()){o.sort(function(a,b){return (b.k.indexOf('gaode')===0)-(a.k.indexOf('gaode')===0)})}var p=pref();if(p){var i=o.findIndex(function(s){return s.k===p});if(i>0)o.unshift(o.splice(i,1)[0])}return o};
var loading=null;
function loadL(){if(window.L)return Promise.resolve();if(loading)return loading;
 loading=new Promise(function(res,rej){var c=d.createElement('link');c.rel='stylesheet';c.href='assets/vendor/leaflet/leaflet.css?v='+V;d.head.appendChild(c);
  var s=d.createElement('script');s.src='assets/vendor/leaflet/leaflet.js?v='+V;s.onload=function(){res()};s.onerror=function(){loading=null;rej()};d.head.appendChild(s)});return loading}
function esc(t){return String(t).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
function init(fig){if(fig._lm)return fig._lm;var pane=fig.querySelector('.mx-pane[data-p=l]'),box=pane.querySelector('.lm'),st=pane.querySelector('.lm-st'),sel=pane.querySelector('.lm-src');
 var D=JSON.parse(fig.getAttribute('data-map')),srcs=order(),cur=-1,layer=null,tried={},markers=[];
 srcs.forEach(function(s,i){var o=d.createElement('option');o.value=i;o.textContent=s.n;sel.appendChild(o)});
 function say(t){st.textContent=t}
 function note(t){var n=fig.querySelector('.mx-note');if(!n){n=d.createElement('div');n.className='mx-note';n.setAttribute('role','status');fig.querySelector('.mx-panes').before(n)}n.textContent=t}
 if(navigator.onLine===false){say('⚠️ 当前离线：请使用上方 🎨 讲解图 / 🏔️ 地形图（本地 SVG，无需网络）');}
 var api={ready:loadL().then(function(){
  var b=D.b,map=L.map(box,{zoomControl:true,scrollWheelZoom:false,tap:true,worldCopyJump:true,attributionControl:true,preferCanvas:true});
  map.fitBounds([[b[2],b[0]],[b[3],b[1]]],{padding:[10,10]});api.map=map;
  map.on('focus',function(){map.scrollWheelZoom.enable()});map.on('blur',function(){map.scrollWheelZoom.disable()});
  D.r.forEach(function(r){L.polyline([r[0],r[1]],{color:r[2],weight:4,opacity:.85,dashArray:'10 8'}).addTo(map)});
  D.m.forEach(function(m,i){var ic=L.divIcon({className:'lm-pin',html:'<span style="--c:'+m[5]+'"><i>'+m[6]+'</i><b>'+(i+1)+'</b></span>',iconSize:[34,34],iconAnchor:[17,17],popupAnchor:[0,-16]});
   var mk=L.marker([m[0],m[1]],{icon:ic,title:m[2],keyboard:true}).addTo(map).bindPopup('<b>'+(i+1)+'. '+esc(m[2])+'</b><br><em>'+esc(m[3])+'</em><br>'+esc(m[4]));markers.push(mk)});
  use(0,false);
 },function(){note('⚠️ 地图引擎加载失败，已切回本地讲解图（离线可用）');fig._switch&&fig._switch('c')})};
 function use(i,auto){if(i>=srcs.length){api.dead=true;say('⚠️ 所有在线底图源都无法连接');note('⚠️ 在线底图暂时无法连接（网络或地区限制），已自动切回本地 🎨 讲解图；🏔️ 地形图同样离线可用。稍后可再点“实时地图”重试。');fig._switch&&fig._switch('c');return}
  var map=api.map,s=srcs[i];cur=i;sel.value=i;tried[i]=1;if(layer)map.removeLayer(layer);
  var ok=0,err=0,t0=Date.now();
  layer=L.tileLayer(s.u,{subdomains:s.s||'abc',attribution:s.a,maxZoom:s.mz,crossOrigin:false,detectRetina:false}).addTo(map);
  layer.on('tileload',function(){ok++;if(ok===1)say('✅ 已连接：'+s.n+(auto?'（自动切换）':''))});
  layer.on('tileerror',function(){err++;if(ok===0&&err>=4&&cur===i){say('⏳ '+s.n+' 无法加载，正在切换下一个源…');next(i)}});
  say('⏳ 正在加载：'+s.n+' …');
  setTimeout(function(){if(cur===i&&ok===0){say('⏳ '+s.n+' 响应超时，自动切换…');next(i)}},7000);
 }
 function next(i){var j=i+1;while(j<srcs.length&&tried[j])j++;use(j,true)}
 sel.addEventListener('change',function(){var i=+sel.value;tried={};setPref(srcs[i].k);api.ready.then(function(){use(i,false)})});
 api.fly=function(i){api.ready.then(function(){var m=markers[i];if(!m)return;api.map.flyTo(m.getLatLng(),Math.max(api.map.getZoom(),D.b[1]-D.b[0]<1?15:7),{duration:.8});m.openPopup()})};
 api.retry=function(){api.dead=false;tried={};var n=fig.querySelector('.mx-note');if(n)n.remove();api.ready.then(function(){use(0,false)})};
 api.resize=function(){api.ready.then(function(){api.map&&api.map.invalidateSize()})};
 fig._lm=api;return api}
window.ProphetsLiveMap={init:init};
})();
