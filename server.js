import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {DatabaseSync} from 'node:sqlite';
import {accountAPI,sessionUser} from './worker/account.js';
const base=path.dirname(fileURLToPath(import.meta.url)),root=path.join(base,'public');
fs.mkdirSync(path.join(base,'data'),{recursive:true});const sqlite=new DatabaseSync(process.env.DATABASE_PATH||path.join(base,'data/accounts.sqlite'));sqlite.exec('PRAGMA foreign_keys = ON');sqlite.exec('CREATE TABLE IF NOT EXISTS _migrations (name TEXT PRIMARY KEY)');
for(const name of fs.readdirSync(path.join(base,'drizzle')).filter(n=>n.endsWith('.sql')).sort()){if(!sqlite.prepare('SELECT name FROM _migrations WHERE name=?').get(name)){sqlite.exec('BEGIN');try{sqlite.exec(fs.readFileSync(path.join(base,'drizzle',name),'utf8'));sqlite.prepare('INSERT INTO _migrations(name) VALUES (?)').run(name);sqlite.exec('COMMIT');}catch(e){sqlite.exec('ROLLBACK');throw e;}}}
const db={prepare(sql){let args=[];return{bind(...values){args=values;return this;},async first(){return sqlite.prepare(sql).get(...args)||null;},async run(){return sqlite.prepare(sql).run(...args);}};}};
const types={'.html':'text/html; charset=utf-8','.css':'text/css','.js':'text/javascript','.png':'image/png','.svg':'image/svg+xml','.pdf':'application/pdf'};
http.createServer(async(req,res)=>{try{const host=req.headers.host||'localhost',protocol=process.env.TRUST_PROXY==='1'&&req.headers['x-forwarded-proto']==='https'?'https':'http';const url=new URL(req.url,`${protocol}://${host}`);const headers=new Headers();for(const[k,v]of Object.entries(req.headers))if(v)headers.set(k,Array.isArray(v)?v.join(','):v);headers.set('x-local-client-ip',req.socket.remoteAddress||'unknown');let body='';if(req.method==='POST')for await(const chunk of req){body+=chunk;if(body.length>8192){res.writeHead(413).end();return;}}const request=new Request(url,{method:req.method,headers,...(req.method==='POST'?{body}:{})});
if(url.pathname.startsWith('/api/')){const response=await accountAPI(request,db);res.writeHead(response.status,Object.fromEntries(response.headers));res.end(await response.text());return;}
let name;try{name=decodeURIComponent(url.pathname);}catch{res.writeHead(400).end();return;}
let dir=root;if(name.startsWith('/downloads/')){if(!await sessionUser(request,db)){res.writeHead(401,{'Cache-Control':'no-store'}).end('Sign in to download this resource.');return;}dir=path.join(base,'private');}
const target=path.resolve(dir,'.'+(name==='/'?'/index.html':name));if(!target.startsWith(dir+path.sep)){res.writeHead(403).end();return;}const stat=await fs.promises.stat(target).catch(()=>null);if(!stat?.isFile()){res.writeHead(404).end('Not found');return;}res.writeHead(200,{'Content-Type':types[path.extname(target)]||'application/octet-stream','X-Content-Type-Options':'nosniff',...(dir!==root?{'Cache-Control':'private, no-store'}:{})});fs.createReadStream(target).pipe(res);}catch(e){console.error(e.message);res.writeHead(503).end('Service temporarily unavailable');}}).listen(Number(process.env.PORT)||3000,'0.0.0.0',()=>console.log('Little Bloom is running'));
