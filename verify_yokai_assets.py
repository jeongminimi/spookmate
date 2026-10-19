"""Read-only audit of the reviewed Yokai image map and the live catalog."""

import json
import os
from pathlib import Path

from dotenv import load_dotenv

from app import _image_name_key, get_db, get_yokai_image_path


ROOT = Path(__file__).resolve().parent


def main() -> int:
    mapping = json.loads((ROOT / "yokai_image_map.json").read_text(encoding="utf-8"))
    ids = [item["source_id"] for item in mapping]
    names = [_image_name_key(item["name"]) for item in mapping]
    missing = [item["image_url"] for item in mapping if not (ROOT / item["image_url"]).is_file()]
    issues = []
    if len(mapping) != 73 or len(set(ids)) != 73 or len(set(names)) != 73:
        issues.append("The local image map does not contain 73 unique IDs and names.")
    issues.extend(f"Missing file: {path}" for path in missing)
    print(f"Local image map: {len(mapping)} entries, {len(missing)} missing files")

    load_dotenv(ROOT / ".env")
    if os.getenv("DATABASE_URL"):
        try:
            conn = get_db()
            try:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT id, name FROM yokai_compendium ORDER BY id")
                    rows = cursor.fetchall()
            finally:
                conn.close()
            print(f"Live database: {len(rows)} records")
            if len(rows) != 73:
                issues.append(f"Expected 73 DB records, got {len(rows)}")
            resolved_images = []
            db_ids = []
            for row in rows:
                db_ids.append(row["id"])
                image = get_yokai_image_path(row["id"], row["name"])
                if not image:
                    issues.append(f"No reviewed image for DB ID {row['id']}: {row['name']}")
                elif not (ROOT / image).is_file():
                    issues.append(f"DB ID {row['id']} maps to missing file: {image}")
                else:
                    resolved_images.append(image)
            if len(set(db_ids)) != len(rows):
                issues.append("The live database has duplicate Yokai IDs.")
            if len(set(resolved_images)) != len(rows):
                issues.append("The live database does not map one-to-one to images.")
        except Exception as error:
            issues.append(f"Live database read failed: {type(error).__name__}")
    else:
        print("Live database: skipped (DATABASE_URL is not configured)")

    for issue in issues:
        print(f"ERROR: {issue}")
    if issues:
        return 1
    print("Path and name checks passed. Visual identity still requires human review.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
