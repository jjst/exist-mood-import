from collections import namedtuple
from datetime import datetime
import csv
import sys
import webbrowser

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

def import_moods_from_csv(csv_file_name):
    with open(csv_file_name) as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)
        mood_tags = headers[7:]
        return [mood_from_row(row, mood_tags) for row in reader]

def authorize_app():
    webbrowser.open('https://exist.io/oauth2/authorize?response_type=code&client_id=%s&scope=%s' % (CLIENT_ID, "read+write"))

def main():
    filename = sys.argv[1]
    authorize_app()
    moods = import_moods_from_csv(filename)

if __name__ == '__main__':
    main()

