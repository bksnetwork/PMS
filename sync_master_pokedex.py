#!/usr/bin/env python3
import json,sqlite3,urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parent; DB=ROOT/"data"/"pokedex.sqlite3"
R={1:("Kanto",1,151),2:("Johto",152,251),3:("Hoenn",252,386),4:("Sinnoh",387,493),5:("Unova",494,649),6:("Kalos",650,721),7:("Alola",722,809),8:("Galar",810,905),9:("Paldea",906,1025)}
def region(n):
 for g,(r,a,b) in R.items():
  if a<=n<=b:return g,r
 return None,None
with sqlite3.connect(DB) as c:
 c.executescript((ROOT/"schema.sql").read_text())
 with urllib.request.urlopen("https://pokeapi.co/api/v2/pokemon-species?limit=2000",timeout=30) as x:d=json.load(x)
 for x in d["results"]:
  n=int(x["url"].rstrip("/").split("/")[-1]); g,r=region(n); name=x["name"].replace("-"," ").title(); img=f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{n}.png"
  c.execute("INSERT INTO species(dex_no,name,generation,region,image_url) VALUES(?,?,?,?,?) ON CONFLICT(dex_no) DO UPDATE SET name=excluded.name,generation=excluded.generation,region=excluded.region,image_url=excluded.image_url",(n,name,g,r,img))
 print("species:",c.execute("select count(*) from species").fetchone()[0])
