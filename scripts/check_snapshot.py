"""Check the two survey exports in this snapshot."""
import csv
from collections import Counter
from pathlib import Path

root = Path(__file__).resolve().parents[1]
with (root / "study_records.csv").open(encoding="utf-8") as source:
    studies = list(csv.DictReader(source))
ids = {row["study_id"] for row in studies}
counts = Counter(row["branch"][0] for row in studies)
with (root / "figure/year_branch.csv").open(encoding="utf-8") as source:
    annual = Counter()
    for row in csv.DictReader(source):
        annual[row["branch"]] += int(row["n"])
if len(studies) != 95 or len(ids) != 95 or counts != annual or counts != dict(A=26, B=17, C=50, D=2):
    raise ValueError("Study identifiers or branch totals differ from the published counts.")
print("95 distinct studies; branch totals agree (26, 17, 50, 2).")
