#!/usr/bin/env python3
"""Structural validator for the connector catalog.

Usage: python scripts/validate.py catalog/connectors.json
"""
import json
import re
import sys

REQUIRED_KEYS = ["id", "name", "vendor", "category", "summary", "status", "version", "events", "auth", "docs"]
ALLOWED_STATUS = {"stable", "beta", "deprecated"}


def fail(msg):
    print("Catalog validation FAILED: " + msg)
    sys.exit(1)


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "catalog/connectors.json"
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as exc:
        fail("could not parse JSON (%s)" % exc)

    if not isinstance(data, dict):
        fail("top level value must be an object")
    for key in ("catalog_version", "updated", "records"):
        if key not in data:
            fail("missing top-level key %r" % key)
    records = data["records"]
    if not isinstance(records, list) or not records:
        fail("'records' must be a non-empty array")

    seen = set()
    for idx, rec in enumerate(records):
        if not isinstance(rec, dict):
            fail("record #%d is not an object" % idx)
        for key in REQUIRED_KEYS:
            if key not in rec:
                fail("record %r is missing required field %r" % (rec.get("id", idx), key))
        rid = rec["id"]
        if not isinstance(rid, str) or not re.match(r"^[a-z0-9]+(-[a-z0-9]+)+$", rid):
            fail("record id %r is not a valid slug" % (rid,))
        if rid in seen:
            fail("duplicate record id %r" % rid)
        seen.add(rid)
        if rec["status"] not in ALLOWED_STATUS:
            fail("record %r has unknown status %r" % (rid, rec["status"]))
        if not isinstance(rec["events"], list) or not rec["events"] or not all(isinstance(e, str) and e for e in rec["events"]):
            fail("record %r events must be a non-empty array of strings" % rid)
        if not isinstance(rec["auth"], list) or not rec["auth"]:
            fail("record %r auth must be a non-empty array" % rid)
        if not isinstance(rec["docs"], str) or not rec["docs"].startswith("docs/connectors/"):
            fail("record %r docs path is invalid" % rid)
        if "repository" in rec and not isinstance(rec["repository"], str):
            fail("record %r repository must be a string" % rid)

    print("Catalog validation OK: %d records, all required fields present, ids unique, JSON well formed." % len(records))


if __name__ == "__main__":
    main()
