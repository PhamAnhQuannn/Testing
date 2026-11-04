import csv
import io


def parse_csv(text):
    rows = [r for r in csv.reader(io.StringIO(text)) if r]
    if not rows:
        return []
    header = rows[0]
    return [dict(zip(header, r)) for r in rows[1:]]
