from random import randint

from faker import Faker

from db import Database


def gen(
    channels_count: int,
    videos_count: int,
    users_count: int,
    comments_count: int,
):
    fake = Faker()

    channels_ids = list(range(1, channels_count + 1))
    channels = [(id, fake.unique.domain_word()) for id in channels_ids]

    videos_ids = list(range(1, videos_count + 1))
    videos = [
        (id, fake.unique.sentence(nb_words=4), randint(1, videos_count))
        for id in videos_ids
    ]

    users_ids = list(range(1, users_count + 1))
    users = [(id, fake.unique.name()) for id in users_ids]

    comments_ids = list(range(1, comments_count + 1))
    comments = [
        (
            id,
            randint(1, users_count),
            randint(1, videos_count),
            fake.unique.sentence(nb_words=9),
            fake.date_between(),
        )
        for id in comments_ids
    ]

    return channels, videos, users, comments


def insert(db: Database, *args):
    channels, videos, users, comments = gen(*args)
    for channel in channels:
        db.add_channel(*channel)
    for video in videos:
        db.add_video(*video)
    for user in users:
        db.add_user(*user)
    for comment in comments:
        db.add_comment(*comment)
