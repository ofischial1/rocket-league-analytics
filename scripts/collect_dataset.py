"""
Phase 2 collection script: pull a larger sample of replays across
multiple rank tiers, flattening each into a row of team-level stats
for later analysis.

Resumable: keeps a log of which replay IDs have already been
processed, so you can stop and restart without redoing work or
hitting duplicate replays.
"""

import os
import json
import time
import csv
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ["BALLCHASING_API_KEY"]
BASE_URL = "https://ballchasing.com/api"
HEADERS = {"Authorization": API_KEY}

RAW_DIR = "raw_replays"
PROCESSED_LOG = "processed_ids.txt"
OUTPUT_CSV = "dataset.csv"

os.makedirs(RAW_DIR, exist_ok=True)

# --- Config: adjust these ---
PLAYLIST = "ranked-standard"       # 3v3 ranked
RANK_TIERS = [
    "gold-1", "platinum-1", "diamond-1",
    "champion-1", "grand-champion-1", "supersonic-legend",
]
REPLAYS_PER_TIER = 100              # start modest, scale up once it's working
REQUEST_DELAY = 1.2                 # seconds between API calls, be polite


def load_processed_ids():
    if not os.path.exists(PROCESSED_LOG):
        return set()
    with open(PROCESSED_LOG) as f:
        return set(line.strip() for line in f if line.strip())


def mark_processed(replay_id):
    with open(PROCESSED_LOG, "a") as f:
        f.write(replay_id + "\n")


def search_replays(rank, count):
    """Page through search results for a given rank tier."""
    results = []
    cursor = None
    while len(results) < count:
        params = {
            "playlist": PLAYLIST,
            "min-rank": rank,
            "max-rank": rank,
            "count": min(200, count - len(results)),  # API max per page is 200
            "sort-by": "replay-date",
            "sort-dir": "desc",
        }
        if cursor:
            params["after"] = cursor

        resp = requests.get(f"{BASE_URL}/replays", headers=HEADERS, params=params)
        resp.raise_for_status()
        data = resp.json()
        batch = data.get("list", [])
        if not batch:
            break  # no more results for this tier
        results.extend(batch)

        cursor = data.get("next")
        if not cursor:
            break
        time.sleep(REQUEST_DELAY)

    return results[:count]


def get_replay_detail(replay_id):
    resp = requests.get(f"{BASE_URL}/replays/{replay_id}", headers=HEADERS)
    resp.raise_for_status()
    return resp.json()


def flatten_replay(replay, rank_tier):
    """
    Turn one replay into two rows (one per team), pulling the
    team-level stats we care about for the analysis.
    """
    rows = []
    for color in ["blue", "orange"]:
        team = replay.get(color)
        if not team or "stats" not in team:
            continue  # incomplete replay, skip this side

        stats = team["stats"]
        won = team.get("stats", {}).get("core", {}).get("goals", 0) > \
              replay.get("orange" if color == "blue" else "blue", {}) \
                    .get("stats", {}).get("core", {}).get("goals", 0)

        row = {
            "replay_id": replay["id"],
            "rank_tier": rank_tier,
            "team_color": color,
            "won": int(replay.get(color, {}).get("stats", {})
                       .get("core", {}).get("shots") is not None and won),
            "avg_boost": stats.get("boost", {}).get("avg_amount"),
            "time_zero_boost": stats.get("boost", {}).get("time_zero_boost"),
            "time_offensive_third": stats.get("positioning", {}).get("time_offensive_third"),
            "time_defensive_third": stats.get("positioning", {}).get("time_defensive_third"),
            "demos_inflicted": stats.get("demo", {}).get("inflicted"),
            "demos_taken": stats.get("demo", {}).get("taken"),
            "shots": stats.get("core", {}).get("shots"),
            "goals": stats.get("core", {}).get("goals"),
            "shooting_pct": stats.get("core", {}).get("shooting_percentage"),
        }
        rows.append(row)

    return rows


def append_rows_to_csv(rows):
    if not rows:
        return
    file_exists = os.path.exists(OUTPUT_CSV)
    with open(OUTPUT_CSV, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        if not file_exists:
            writer.writeheader()
        writer.writerows(rows)


def main():
    processed = load_processed_ids()
    print(f"Resuming with {len(processed)} replays already processed.\n")

    for rank in RANK_TIERS:
        print(f"=== Collecting {REPLAYS_PER_TIER} replays for rank: {rank} ===")
        try:
            summaries = search_replays(rank, REPLAYS_PER_TIER)
        except requests.HTTPError as e:
            print(f"  Error searching {rank}: {e}")
            continue

        print(f"  Found {len(summaries)} candidate replays.")

        for i, summary in enumerate(summaries):
            replay_id = summary["id"]
            if replay_id in processed:
                continue  # already handled in a previous run

            try:
                detail = get_replay_detail(replay_id)
            except requests.HTTPError as e:
                print(f"  [{i+1}/{len(summaries)}] Failed on {replay_id}: {e}")
                time.sleep(REQUEST_DELAY)
                continue

            # Save raw JSON in case we want to re-derive different features later
            with open(os.path.join(RAW_DIR, f"{replay_id}.json"), "w") as f:
                json.dump(detail, f)

            rows = flatten_replay(detail, rank)
            append_rows_to_csv(rows)
            mark_processed(replay_id)
            processed.add(replay_id)

            if (i + 1) % 10 == 0:
                print(f"  [{i+1}/{len(summaries)}] processed...")

            time.sleep(REQUEST_DELAY)

        print(f"  Done with {rank}.\n")

    print(f"All done. Dataset written to {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
