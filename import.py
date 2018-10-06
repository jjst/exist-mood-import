import sys
import requests, json
import auth
import operator
import imoodjournal
import daylio


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
    try:
        mood_data = imoodjournal.import_csv(mood_data_file)
    except ValueError:
        mood_data = daylio.import_csv(mood_data_file)
    attrs = ["mood", "mood_note", "custom"]
    try:
        acquire_attrs(attrs, token)
        publish_data(mood_data, token)
    finally:
        release_attrs(attrs, token)


def main():
    filename = sys.argv[1]
    token = auth.token()
    do_import(filename, token)

if __name__ == '__main__':
    main()

