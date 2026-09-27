#!/usr/bin/env python3
import json,mimetypes,sqlite3
from http.server import ThreadingHTTPServer,BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse,parse_qs
ROOT=Path(__file__).resolve().parent; DB=ROOT/"data"/"pokedex.sqlite3"; STATIC=ROOT/"static"
def db():
 c=sqlite3.connect(DB); c.row_factory=sqlite3.Row; c.execute("PRAGMA foreign_keys=ON"); return c
def init():
 DB.parent.mkdir(parents=True,exist_ok=True); c=db(); c.executescript((ROOT/"schema.sql").read_text())
 if c.execute("SELECT COUNT(*) FROM pokemon").fetchone()[0]==0:
  s=json.loads((ROOT/"data"/"seed.json").read_text())
  for p in s["pokemon"]:
   dex=p.pop("dex_no"); name=p.pop("name")
   c.execute("INSERT OR IGNORE INTO species(dex_no,name,image_url) VALUES(?,?,?)",(dex,name,f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{dex}.png"))
   ks=list(p); c.execute(f"INSERT INTO pokemon(dex_no,{','.join(ks)}) VALUES(?,{','.join(['?']*len(ks))})",[dex]+[p[k] for k in ks])
  for r in s["resources"]:
   ks=list(r); c.execute(f"INSERT OR REPLACE INTO resources({','.join(ks)}) VALUES({','.join(['?']*len(ks))})",[r[k] for k in ks])
  c.commit()
 c.close()
class H(BaseHTTPRequestHandler):
 def json(self,o,s=200):
  b=json.dumps(o,ensure_ascii=False).encode(); self.send_response(s); self.send_header("Content-Type","application/json"); self.send_header("Content-Length",str(len(b))); self.end_headers(); self.wfile.write(b)
 def do_GET(self):
  u=urlparse(self.path)
  if u.path=="/api/pokemon":
   c=db(); q=parse_qs(u.query).get("q",[""])[0]; rows=[dict(r) for r in c.execute("SELECT p.*,s.name,s.image_url FROM pokemon p JOIN species s USING(dex_no) WHERE p.action_status!='TRANSFERRED' AND (s.name LIKE ? OR CAST(p.dex_no AS TEXT) LIKE ?) ORDER BY p.dex_no,p.cp DESC",(f"%{q}%",f"%{q}%"))]; c.close(); return self.json(rows)
  if u.path=="/api/resources":
   c=db(); rows=[dict(r) for r in c.execute("SELECT * FROM resources ORDER BY resource_type,display_name")]; c.close(); return self.json(rows)
  if u.path=="/api/dashboard":
   c=db(); out={"tracked":c.execute("SELECT COUNT(*) FROM pokemon WHERE action_status!='TRANSFERRED'").fetchone()[0],"species":c.execute("SELECT COUNT(DISTINCT dex_no) FROM pokemon WHERE action_status!='TRANSFERRED'").fetchone()[0]}; c.close(); return self.json(out)
  p=STATIC/("index.html" if u.path=="/" else u.path.lstrip("/"))
  if not p.exists(): return self.send_error(404)
  b=p.read_bytes(); self.send_response(200); self.send_header("Content-Type",mimetypes.guess_type(p.name)[0] or "application/octet-stream"); self.send_header("Content-Length",str(len(b))); self.end_headers(); self.wfile.write(b)
if __name__=="__main__":
 init(); print("PMS: http://127.0.0.1:8765"); ThreadingHTTPServer(("127.0.0.1",8765),H).serve_forever()
