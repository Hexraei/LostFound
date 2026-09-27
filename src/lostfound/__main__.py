"""Match synthetic or coordinator-redacted reports; never send mail or release items."""
import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path

REQUIRED = {"id", "direction", "category", "place", "date"}
FORBIDDEN = {"name", "email", "phone", "address", "serial", "serial_number", "secret", "verification_answer", "body", "recipient", "from", "to"}


def norm(value):
    return " ".join(re.findall(r"[a-z0-9]+", value.lower()))


def validate(raw):
    if not isinstance(raw, dict) or not isinstance(raw.get("reports"), list):
        raise ValueError("Expected object with reports array")
    seen = set()
    out = []
    for i, row in enumerate(raw["reports"]):
        if not isinstance(row, dict) or not REQUIRED <= row.keys():
            raise ValueError(f"Report {i}: missing required fields")
        if FORBIDDEN & row.keys():
            raise ValueError(f"Report {i}: private/unsafe fields are not allowed")
        if any(not isinstance(row[k], str) or not row[k].strip() for k in REQUIRED):
            raise ValueError(f"Report {i}: empty/non-text required field")
        if row["id"] in seen:
            raise ValueError(f"Report {i}: duplicate ID")
        seen.add(row["id"])
        if row["direction"] not in ("lost", "found"):
            raise ValueError(f"Report {i}: direction must be lost or found")
        if not isinstance(row.get("sensitive", False), bool):
            raise ValueError(f"Report {i}: sensitive must be boolean")
        if row.keys() - (REQUIRED | {"public_description", "sensitive"}):
            raise ValueError(f"Report {i}: unexpected fields")
        if "public_description" in row and not isinstance(row["public_description"], str):
            raise ValueError(f"Report {i}: public_description must be text")
        try:
            date = dt.date.fromisoformat(row["date"])
        except ValueError as exc:
            raise ValueError(f"Report {i}: invalid date") from exc
        if date.isoformat() != row["date"]:
            raise ValueError(f"Report {i}: date must be YYYY-MM-DD")
        out.append({**row, "_date": date})
    return out


def match(reports):
    lost = [r for r in reports if r["direction"] == "lost" and not r.get("sensitive")]
    found = [r for r in reports if r["direction"] == "found" and not r.get("sensitive")]
    candidates = []
    for a in lost:
        for b in found:
            if norm(a["category"]) != norm(b["category"]):
                continue
            days = abs((a["_date"] - b["_date"]).days)
            if days > 3 or norm(a["place"]) != norm(b["place"]):
                continue
            candidates.append({"lost_id": a["id"], "found_id": b["id"],
                               "category": a["category"], "place": a["place"],
                               "days_apart": days, "rank": 3 - days,
                               "status": "candidate_staff_review"})
    return sorted(candidates, key=lambda x: (-x["rank"], x["lost_id"], x["found_id"]))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("match", choices=["match"])
    parser.add_argument("--input", required=True, type=Path)
    args = parser.parse_args()
    try:
        data = validate(json.loads(args.input.read_text()))
        print(json.dumps({"reviewed": len(data), "candidates": match(data)}, indent=2))
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        print(f"Invalid report set: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
