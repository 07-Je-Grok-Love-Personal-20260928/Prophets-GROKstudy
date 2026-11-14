/* 先知书 v2 · 离线缓存：页面 network-first（断网回退缓存），资源 stale-while-revalidate（资源带 ?v= 版本号）。外部瓦片/视频不缓存。 */
var C='prophets-'+(new URL(self.location).searchParams.get('v')||'v2');
self.addEventListener('install',function(){self.skipWaiting()});
self.addEventListener('activate',function(e){e.waitUntil(caches.keys().then(function(ks){return Promise.all(ks.filter(function(k){return k.indexOf('prophets-')===0&&k!==C}).map(function(k){return caches.delete(k)}))}).then(function(){return self.clients.claim()}))});
self.addEventListener('fetch',function(e){var r=e.request;if(r.method!=='GET')return;var u=new URL(r.url);if(u.origin!==self.location.origin)return;
 if(r.mode==='navigate'){e.respondWith(caches.open(C).then(function(c){return fetch(r).then(function(res){if(res&&res.ok)c.put(r,res.clone());return res}).catch(function(){return c.match(r).then(function(h){return h||c.match('index.html')})})}));return}
 e.respondWith(caches.open(C).then(function(c){return c.match(r).then(function(hit){var net=fetch(r).then(function(res){if(res&&res.ok)c.put(r,res.clone());return res}).catch(function(){return hit});return hit||net})}))});
