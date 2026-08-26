"""
Phase 1 test pull: confirm API access and inspect the shape of the data
before building the full collection pipeline.
"""

import os
import json
import time
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ["BALLCHASING_API_KEY"]
BASE_URL = "https://ballchasing.com/api"
HEADERS = {"Authorization": API_KEY}

OUTPUT_DIR = "raw_replays"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def search_replays(playlist="ranked-standard", rank="diamond-1", count=20):
    """Pull a small batch of replay summaries to test filtering."""
    params = {
        "playlist": playlist,
        "min-rank": rank,
        "max-rank": rank,
        "count": count,
        "sort-by": "replay-date",
        "sort-dir": "desc",
    }
    resp = requests.get(f"{BASE_URL}/replays", headers=HEADERS, params=params)
    resp.raise_for_status()
    return resp.json()["list"]


def get_replay_detail(replay_id):
    """Pull the full stats blob for a single replay."""
    resp = requests.get(f"{BASE_URL}/replays/{replay_id}", headers=HEADERS)
    resp.raise_for_status()
    return resp.json()


def main():
    print("Searching for a small batch of replays...")
    replays = search_replays(count=10)
    print(f"Found {len(replays)} replays.")

    if not replays:
        print("No replays found — try loosening the rank/playlist filters.")
        return

    # Pull full detail for just the first few, so we can inspect the fields
    for i, r in enumerate(replays[:3]):
        replay_id = r["id"]
        print(f"Fetching detail for replay {replay_id} ({i+1}/3)...")
        detail = get_replay_detail(replay_id)

        out_path = os.path.join(OUTPUT_DIR, f"{replay_id}.json")
        with open(out_path, "w") as f:
            json.dump(detail, f, indent=2)
        print(f"  Saved to {out_path}")

        # Ballchasing rate limit is generous but be polite
        time.sleep(1)

    print("\nDone. Open one of the saved JSON files and look for these keys:")
    print("  - blue/orange team stats (boost, positioning, demos, etc.)")
    print("  - players[] list for per-player breakdowns")
    print("  - duration, map, playlist metadata")


if __name__ == "__main__":
    main()
