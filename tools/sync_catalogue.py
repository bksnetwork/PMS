#!/usr/bin/env python3
"""Synchronize TCGplayer public catalogue snapshots via tcgcsv; fail closed on errors."""
import json, re, time, urllib.request, sys
from pathlib import Path
from datetime import datetime, timezone
ROOT=Path(__file__).resolve().parent.parent/"catalogue"
BASE="https://tcgcsv.com/tcgplayer/"
def get(url):
    for attempt in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":"CardCatalogue/2.0"}),timeout=45) as response:
                obj=json.load(response)
            if not isinstance(obj,dict) or not isinstance(obj.get("results"),list):
                raise ValueError("Unexpected data format")
            return obj["results"]
        except Exception:
            if attempt==2: raise
            time.sleep(2*(attempt+1))
def run():
    cfg=json.loads((ROOT/"sets.json").read_text())
    groups=get(f'{BASE}{cfg["category"]}/groups')
    staged=[]
    failures=[]
    print("Available relevant groups:", [(g["groupId"],g["name"]) for g in groups if re.search(r"30th|celebration|classic|delta|promo",g["name"],re.I)])
    for spec in cfg["sets"]:
        try:
            matches=[]
            for rule in spec["groups"]:
                pattern=rule["match"]
                found=[g for g in groups if re.fullmatch(pattern,g["name"],re.I)]
                if len(found)!=1:
                    raise ValueError(f'{spec["id"]}: expected exactly one group matching {pattern!r}, got {len(found)}')
                if any(g["groupId"]==found[0]["groupId"] for g,_ in matches):
                    raise ValueError("Duplicate group")
                matches.append((found[0],rule["role"]))
            cards=[]
            for group,role in matches:
                gid=group["groupId"]; prices={}
                for p in get(f'{BASE}{cfg["category"]}/{gid}/prices'):
                    m=p.get("marketPrice")
                    prices.setdefault(p["productId"],[]).append({"t":p.get("subTypeName") or "Normal","m":m if isinstance(m,(int,float)) and m>=0 else None})
                for p in get(f'{BASE}{cfg["category"]}/{gid}/products'):
                    ext={e["name"]:e["value"] for e in p.get("extendedData",[]) if "name" in e and "value" in e}
                    if not ext.get("Number"): continue
                    cards.append({"pid":p["productId"],"name":p.get("cleanName") or p["name"],"num":ext["Number"],"rarity":ext.get("Rarity",""),"img":p.get("imageUrl",""),"role":role,"prints":prices.get(p["productId"]) or [{"t":"Normal","m":None}]})
            if not cards: raise ValueError(f'{spec["id"]}: empty card list; refusing to overwrite')
            staged.append((spec["id"],{"id":spec["id"],"name":spec["name"],"updated":datetime.now(timezone.utc).isoformat(),"cards":cards}))
        except (ValueError, KeyError, TypeError) as exc:
            failures.append(f"{spec['id']}: {exc}")
            print("SKIPPED:", failures[-1], file=sys.stderr)
    dest=ROOT/"data";dest.mkdir(exist_ok=True)
    if not staged:
        raise ValueError("No valid sets; existing data preserved. " + "; ".join(failures))
    existing=[]
    idx=dest/"index.json"
    if idx.exists():
        existing=json.loads(idx.read_text())
    for sid,data in staged:
        (dest/f"{sid}.json").write_text(json.dumps(data,ensure_ascii=False))
    merged={item["id"]:item for item in existing if (dest/(item["id"]+".json")).exists()}
    merged.update({sid:{"id":sid,"name":data["name"]} for sid,data in staged})
    idx.write_text(json.dumps(list(merged.values()),ensure_ascii=False))
    if failures:
        print("Partial update; unresolved sets:", "; ".join(failures), file=sys.stderr)
if __name__=="__main__": run()
