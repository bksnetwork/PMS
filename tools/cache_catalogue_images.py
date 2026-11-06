#!/usr/bin/env python3
"""Cache card images for the GitHub Pages gallery, preserving source URLs on failures."""
import json
import re
import time
import urllib.request
from pathlib import Path
from urllib.parse import urlparse

ROOT=Path(__file__).resolve().parents[1]/"catalogue"
DATA=ROOT/"data"
CACHE=ROOT/"images"
MAX_BYTES=1_500_000
def cache():
    idx=DATA/"index.json"
    if not idx.exists(): raise RuntimeError("Run data synchronization first")
    sets=json.loads(idx.read_text())
    changed=0
    for entry in sets:
        path=DATA/(entry["id"]+".json")
        data=json.loads(path.read_text())
        folder=CACHE/entry["id"]
        folder.mkdir(parents=True,exist_ok=True)
        for card in data["cards"]:
            url=card.get("sourceImage") or card.get("img") or ""
            if url.startswith("images/"): continue
            if not url.startswith("https://"): continue
            parsed=urlparse(url)
            if parsed.hostname not in ("tcgplayer-cdn.tcgplayer.com","product-images.tcgplayer.com","tcgplayer.com","www.tcgplayer.com"):
                continue
            filename=str(card["pid"])+".jpg"
            target=folder/filename
            if not target.exists():
                try:
                    req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0 CardCatalogueImageCache/1.0"})
                    with urllib.request.urlopen(req,timeout=20) as response:
                        typ=response.headers.get("Content-Type","")
                        if not typ.startswith("image/"): continue
                        payload=response.read(MAX_BYTES+1)
                    if len(payload)>MAX_BYTES or len(payload)<100: continue
                    target.write_bytes(payload)
                    changed+=1
                except Exception as exc:
                    print("Image skipped",card["pid"],str(exc)[:90])
                    continue
                time.sleep(.05)
            card["sourceImage"]=url
            card["img"]="images/"+entry["id"]+"/"+filename
        path.write_text(json.dumps(data,ensure_ascii=False))
    print("New cached images:",changed)
if __name__=="__main__": cache()
