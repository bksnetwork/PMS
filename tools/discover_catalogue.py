#!/usr/bin/env python3
"""Read-only catalogue discovery: list potential TCGcsv group matches without guessing."""
import json
import re
import sys
import urllib.request
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]/"catalogue"
URL="https://tcgcsv.com/tcgplayer/3/groups"
PATTERNS={
    "30th-celebrations":r"30th|anniversary|celebrat",
    "delta-reign":r"delta|reign",
}
def discover(groups):
    result={}
    for slug,pattern in PATTERNS.items():
        result[slug]=[
            {"groupId":g.get("groupId"),"name":g.get("name")}
            for g in groups
            if isinstance(g,dict) and re.search(pattern,str(g.get("name","")),re.I)
        ]
    return result
def main():
    request=urllib.request.Request(URL,headers={"User-Agent":"CardCatalogue/3.0"})
    with urllib.request.urlopen(request,timeout=45) as response:
        payload=json.load(response)
    groups=payload.get("results")
    if not isinstance(groups,list): raise ValueError("Invalid groups payload")
    report={"source":URL,"candidates":discover(groups),"requiresHumanVerification":True}
    output=ROOT/"data"/"discovery.json"
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(report,indent=2))
    print(json.dumps(report,indent=2))
    if not any(report["candidates"].values()):
        print("No matching groups; do not substitute unrelated sets.",file=sys.stderr)
if __name__=="__main__":
    main()
