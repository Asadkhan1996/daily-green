#!/usr/bin/env python3
import os, random, subprocess
from datetime import datetime, timedelta, timezone

DAYS = 365                 # how far back to fill
MIN_COMMITS = 1            # per day
MAX_COMMITS = 3            # per day

def sh(cmd, env=None):
    subprocess.check_call(cmd, shell=True, env=env)

for i in range(DAYS, 0, -1):
    # target day at 12:00 UTC to avoid day-boundary shifts
    dt = (datetime.now(timezone.utc) - timedelta(days=i)).replace(hour=12, minute=0, second=0, microsecond=0)
    ds = dt.strftime("%Y-%m-%dT%H:%M:%S%z")  # ISO8601 w/ offset, e.g. 2025-08-14T12:00:00+0000

    commits_today = random.randint(MIN_COMMITS, MAX_COMMITS)
    for n in range(commits_today):
        with open("log.txt", "a", encoding="utf-8") as f:
            f.write(f"{dt.date()} commit {n+1}\n")

        env = os.environ.copy()
        env["GIT_AUTHOR_DATE"] = ds
        env["GIT_COMMITTER_DATE"] = ds
        sh('git add log.txt', env=env)
        sh(f'git commit -m "log {dt.date()} #{n+1}"', env=env)

print("Done creating backfill commits.")
