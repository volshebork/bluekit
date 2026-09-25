# This module defines the shared logs layout and archives previous results into history.

from datetime import datetime
from pathlib import Path

# variables
logs_dir = Path(__file__).resolve().parents[2] / "logs"  # bluekit/logs; human-readable output
raw_dir = logs_dir / "raw"  # machine-readable output used by other modules
history_dir = logs_dir / "history"  # previous results; mirrors the layout of logs/


def archive_previous(*files):
    # move previous results into history, all stamped with when that scan ran
    existing = [f for f in files if f.exists()]
    if not existing:
        return  # nothing to archive (e.g. first run)

    timestamp = datetime.fromtimestamp(existing[0].stat().st_mtime).strftime("%Y-%m-%d_%H%M%S")

    # each file keeps its place relative to logs/ (logs/raw/x.xml -> logs/history/raw/x_<timestamp>.xml)
    for file in existing:
        dest_dir = history_dir / file.parent.relative_to(logs_dir)
        dest_dir.mkdir(parents=True, exist_ok=True)
        file.replace(dest_dir / f"{file.stem}_{timestamp}{file.suffix}")