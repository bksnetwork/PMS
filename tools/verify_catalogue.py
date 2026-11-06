#!/usr/bin/env python3
"""Validate catalogue snapshots before publishing them."""
import json
import math
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1] / "catalogue"
DATA = ROOT / "data"

def validate():
    errors = []
    index_path = DATA / "index.json"
    if not index_path.exists():
        return ["Missing catalogue/data/index.json"]
    try:
        index = json.loads(index_path.read_text(encoding="utf-8"))
    except (ValueError, OSError) as exc:
        return [f"Invalid index: {exc}"]
    if not isinstance(index, list) or not index:
        return ["Index must contain at least one set"]
    seen_sets = set()
    for entry in index:
        sid = entry.get("id") if isinstance(entry, dict) else None
        if not isinstance(sid, str) or not re.fullmatch(r"[a-z0-9][a-z0-9-]*", sid):
            errors.append(f"Invalid set identifier: {sid!r}")
            continue
        if sid in seen_sets:
            errors.append(f"Duplicate set: {sid}")
        seen_sets.add(sid)
        path = DATA / f"{sid}.json"
        try:
            record = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            errors.append(f"{sid}: cannot read set: {exc}")
            continue
        cards = record.get("cards")
        if record.get("id") != sid or not isinstance(cards, list) or not cards:
            errors.append(f"{sid}: missing cards or mismatched id")
            continue
        seen_products = set()
        for card in cards:
            pid = card.get("pid")
            if not isinstance(pid, int) or pid <= 0 or pid in seen_products:
                errors.append(f"{sid}: duplicate or invalid product id {pid!r}")
            seen_products.add(pid)
            if not all(isinstance(card.get(k), str) and card[k].strip() for k in ("name", "num", "role")):
                errors.append(f"{sid}/{pid}: missing card name, number or role")
            if card.get("role") not in ("main", "master", "grand"):
                errors.append(f"{sid}/{pid}: invalid role")
            prints = card.get("prints")
            if not isinstance(prints, list) or not prints:
                errors.append(f"{sid}/{pid}: missing print variants")
                continue
            seen_prints = set()
            for variant in prints:
                label = variant.get("t")
                if not isinstance(label, str) or not label or label in seen_prints:
                    errors.append(f"{sid}/{pid}: duplicate or missing variant")
                seen_prints.add(label)
                market = variant.get("m")
                if market is not None and (not isinstance(market, (int, float)) or isinstance(market, bool) or not math.isfinite(market) or market < 0):
                    errors.append(f"{sid}/{pid}/{label}: invalid market price")
        print(f"{sid}: {len(cards)} products checked")
    return errors

if __name__ == "__main__":
    failures = validate()
    if failures:
        print("\n".join(failures), file=sys.stderr)
        sys.exit(1)
    print("Catalogue validation passed")
