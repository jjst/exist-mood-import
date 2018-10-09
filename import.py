#!/usr/bin/python3

import sys
import requests, json
import auth
import imoodjournal
import daylio
import os
import itertools


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

def attributes(mood):
    def create_attr(name, value, date):
        date_format = '%Y-%m-%d'
        return {"name": name, "date": date.strftime(date_format), "value": value}
    attrs = [create_attr("mood", mood.level, mood.date)]
    if mood.comment:
        attrs.append(create_attr("mood_note", mood.comment, mood.date))
    if mood.tags:
        attrs.append(create_attr("custom", ", ".join(mood.tags), mood.date))
    return attrs

def group(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return itertools.zip_longest(*args, fillvalue=fillvalue)

def publish_data(moods, token):
    attrs = []
    for mood in moods:
        attrs += attributes(mood)
    url = 'https://exist.io/api/1/attributes/update/'
    response = requests.post(url, headers={'Authorization':f"Bearer {token}"},
        json=attrs)
    return response


def do_import(mood_data_file, token):
    try:
        mood_data = imoodjournal.import_csv(mood_data_file)
        data_type = "imoodjournal"
    except ValueError:
        mood_data = daylio.import_csv(mood_data_file)
        data_type = "daylio"
    print(f"Loaded {data_type} data. Starting import...")
    attrs = ["mood", "mood_note", "custom"]
    try:
        acquire_attrs(attrs, token)
        chunk_size = 5
        chunk_count = (len(mood_data) // chunk_size) + 1
        for (i, moods) in enumerate(group(mood_data, chunk_size)):
            res = publish_data(moods, token)
            if res.status_code != 200:
                print(f"Error sending request {res.json()}")
            else:
                json = res.json()
                failed = json['failed']
                if failed:
                    print(f"Some attributes failed to publish: {failed}")
                success = json['success']
                if success:
                    print(f"Successfully published attributes [chunk {i + 1}/{chunk_count}]:")
                    print("\n".join("  - " + str(a) for a in success))
        print("Finished import.")
    finally:
        release_attrs(attrs, token)


def main():
    try:
        filename = sys.argv[1]
    except IndexError:
        print(f"Usage: {sys.argv[0]} <daylio_or_imoodjournal_export.csv>")
        sys.exit(1)
    token = os.environ.get("ACCESS_TOKEN") or auth.token()
    do_import(filename, token)

if __name__ == '__main__':
    main()

