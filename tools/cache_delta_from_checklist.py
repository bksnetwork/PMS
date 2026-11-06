#!/usr/bin/env python3
"""Cache Delta Reign images by matching the numbered Portal TCG checklist."""
import json
import re
import urllib.request
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/"catalogue/data/delta-reign.json"
IMAGES=ROOT/"catalogue/images/delta-reign"
URL="https://portaltcg.co.uk/collections/delta-reign"

class Parser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.images={}
    def handle_starttag(self,tag,attrs):
        if tag!="img":return
        attrs=dict(attrs)
        alt=attrs.get("alt","")
        match=re.search(r"\b(\d{3})/103\b",alt)
        if not match:return
        src=attrs.get("data-src") or attrs.get("src") or ""
        if not src or src.startswith("data:"):return
        self.images.setdefault(int(match.group(1)),urljoin(URL,src))

def main():
    request=urllib.request.Request(URL,headers={"User-Agent":"Mozilla/5.0"})
    with urllib.request.urlopen(request,timeout=30) as response:
        markup=response.read(7000000).decode("utf-8","replace")
    parser=Parser()
    parser.feed(markup)
    print("Numbered source images:",len(parser.images))
    if len(parser.images)<90:
        raise RuntimeError("Fewer than 80 numbered source images; refusing incomplete update")
    data=json.loads(DATA.read_text())
    IMAGES.mkdir(parents=True,exist_ok=True)
    success=0
    for card in data["cards"]:
        match=re.match(r"^(\d{1,3})/103$",str(card.get("num","")))
        if not match:continue
        number=int(match.group(1))
        url=parser.images.get(number)
        if not url:continue
        dest=IMAGES/(str(card["pid"])+".jpg")
        existing=next((p for p in (dest, dest.with_suffix(".png"),dest.with_suffix(".webp")) if p.exists()),None)
        if existing:dest=existing
        else:
            try:
                req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0","Referer":URL})
                with urllib.request.urlopen(req,timeout=20) as response:
                    payload=response.read(2000001)
                    content_type=response.headers.get("Content-Type","")
                if len(payload)>2000000 or len(payload)<1500:
                    continue
                if payload.startswith(bytes([255,216,255])):
                    suffix=".jpg"
                elif payload.startswith(bytes([137,80,78,71,13,10,26,10])):
                    suffix=".png"
                elif payload[:4]==b"RIFF" and payload[8:12]==b"WEBP":
                    suffix=".webp"
                else:
                    print("Unsupported image format:",number,content_type)
                    continue
                dest=dest.with_suffix(suffix)
                dest.write_bytes(payload)
            except Exception as error:
                print("Download failed:",number,str(error)[:100])
                continue
        card["sourceImage"]=url
        card["img"]="images/delta-reign/"+dest.name
        card["imageSource"]=URL
        success+=1
    if success<80:raise RuntimeError("Too few images cached: "+str(success))
    DATA.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n")
    print("Locally cached images:",success)

if __name__=="__main__":main()
