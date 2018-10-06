import csv
from mood import Mood
from datetime import datetime

mood_levels = {
    'rad': 5,
    'good': 4,
    'meh': 3,
    'bad': 2,
    'awful': 1
}

def mood_from_row(row):
    year = row[0]
    day_and_month = row[1]
    date_string = f'{day_and_month} {year}'
    try:
        d = datetime.strptime(date_string, '%d %B %Y')
    except ValueError as e:
        return None
    level = mood_levels[row[4].strip()]
    tags = set([t.strip().replace(' ', '_') for t in row[5].strip().split(' | ')])
    return Mood(date=d, level=level, comment=row[6], tags=tags)

def import_csv(csv_file_name):
    with open(csv_file_name) as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)
        all_moods = [mood_from_row(row) for row in reader]
        return all_moods
