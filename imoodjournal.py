from collections import namedtuple
from datetime import datetime
import csv
import sys
import requests, json
import auth
import operator
import itertools


Mood = namedtuple('Mood', ['date', 'level', 'comment', 'tags'])

MoodData = namedtuple('MoodData', ['mood_tags', 'moods'])

def combine(date, moods):
    moods = list(moods)
    new_level = sum(m.level for m in moods) // len(moods)
    tags = set(tag for m in moods for tag in m.tags)
    comment = ' '.join(m.comment for m in moods).strip()
    return Mood(date, new_level, comment, tags)

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

def import_moods_from_csv(csv_file_name):
    with open(csv_file_name) as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)
        mood_tags = headers[7:]
        all_moods = [mood_from_row(row, mood_tags) for row in reader]
        unique_moods_per_day = [combine(date, moods) for (date, moods) in itertools.groupby(all_moods, operator.attrgetter('date'))]
        return MoodData(mood_tags, unique_moods_per_day)

def acquire_attrs(attributes, token):
    url = 'https://exist.io/api/1/attributes/acquire/'

    attrs = [{"name": a, "active": True} for a in attributes]

    response = requests.post(url, headers={'Authorization':f"Bearer {token}"},
        json=attrs)
    return response

def release_attrs(attributes, token):
    url = 'https://exist.io/api/1/attributes/release/'

    attrs = [{"name": a} for a in attributes]

    response = requests.post(url, headers={'Authorization':f"Bearer {token}"},
        json=attrs)
    return response

def publish_data(moods, token):
    for mood in moods:
        response = publish_one(mood, token)
        print(response)
        print(response.json())


def publish_one(mood, token):
    url = 'https://exist.io/api/1/attributes/update/'
    def create_attr(name, value, date):
        date_format = '%Y-%m-%d'
        return {"name": name, "date": date.strftime(date_format), "value": value}
    def attributes(mood):
        attrs = [create_attr("mood", mood.level, mood.date)]
        if mood.comment:
            attrs.append(create_attr("mood_note", mood.comment, mood.date))
        if mood.tags:
            attrs.append(create_attr("custom", ", ".join(mood.tags), mood.date))
        return attrs
    response = requests.post(url, headers={'Authorization':f"Bearer {token}"},
        json=attributes(mood))
    return response



def do_import(mood_data_file, token):
    mood_data = import_moods_from_csv(mood_data_file)
    attrs = ["mood", "mood_note", "custom"]
    try:
        acquire_attrs(attrs, token)
        publish_data(mood_data.moods, token)
    finally:
        release_attrs(attrs, token)


def main():
    filename = sys.argv[1]
    token = auth.token()
    do_import(filename, token)

if __name__ == '__main__':
    main()

