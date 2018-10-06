from collections import namedtuple

Mood = namedtuple('Mood', ['date', 'level', 'comment', 'tags'])

MoodData = namedtuple('MoodData', ['mood_tags', 'moods'])

def combine(date, moods):
    moods = list(moods)
    new_level = sum(m.level for m in moods) // len(moods)
    tags = set(tag for m in moods for tag in m.tags)
    comment = ' '.join(m.comment for m in moods).strip()
    return Mood(date, new_level, comment, tags)

