from collections import namedtuple
from datetime import datetime

Mood = namedtuple('Mood', ['date', 'level', 'comment', 'tags'])

def mood_from_row(row, mood_tags):
    date_string = row[0]
    try:
        d = datetime.strptime(date_string, '%d %B %Y')
    except ValueError as e:
        return None
    active_tags = [int(i) for i in row[7:]]
    active_indices = [i for (i, t) in enumerate(active_tags) if t == 1]
    tags = [mood_tags[i] for i in active_indices]
    return Mood(date=d, level=int(row[4]), comment=row[6], tags=tags)

if __name__ == '__main__':
    with open('iMoodJournal.csv') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)
        mood_tags = headers[7:]
        print(mood_tags)
        for row in reader:
            print(mood_from_row(row, mood_tags))
