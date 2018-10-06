from mood import Mood
import csv
from datetime import datetime
import itertools

def mood_from_row(row, mood_tags):
    date_string = row[0]
    try:
        d = datetime.strptime(date_string, '%d %B %Y')
    except ValueError as e:
        return None
    active_tags = [int(i) for i in row[7:]]
    active_indices = [i for (i, t) in enumerate(active_tags) if t == 1]
    tags = set([mood_tags[i] for i in active_indices])
    normalized_level = int(row[4]) // 2
    return Mood(date=d, level=normalized_level, comment=row[6], tags=tags)

def import_csv(csv_file_name):
    with open(csv_file_name, encoding='utf-8-sig') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)
        expected_headers = ["Date","Day of week","Hour","Minute","Level","LevelText","Comment"]
        actual_headers = [h.strip() for h in headers[:7]]
        if actual_headers != expected_headers:
            raise ValueError(f"Unexpected headers: {actual_headers}. Is this a valid iMoodJournal export?")
        mood_tags = headers[7:]
        all_moods = [mood_from_row(row, mood_tags) for row in reader]
        unique_moods_per_day = [combine(date, moods) for (date, moods) in itertools.groupby(all_moods, operator.attrgetter('date'))]
        return unique_moods_per_day
