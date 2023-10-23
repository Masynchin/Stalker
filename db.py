import datetime as dt
import sqlite3
from contextlib import contextmanager
from typing import Self


class Database:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    @classmethod
    @contextmanager
    def initialize(cls, path) -> Self:
        with sqlite3.connect(path) as conn:
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    username TEXT
                );

                CREATE TABLE IF NOT EXISTS videos (
                    id INTEGER PRIMARY KEY,
                    title TEXT,
                    channel_id INTEGER REFERENCES channels(id)
                );
                CREATE TABLE IF NOT EXISTS comments (
                    id INTEGER PRIMARY KEY,
                    author_id INTEGER REFERENCES users(id),
                    video_id INTEGER REFERENCES videos(id),
                    content TEXT,
                    created_at DATETIME
                );
                CREATE TABLE IF NOT EXISTS channels (
                    id INTEGER PRIMARY KEY,
                    name TEXT
                );
                """
            )
            yield cls(conn)

    def add_user(self, id: int, username: str):
        self.conn.execute(
            "INSERT INTO users(id, username) VALUES(?, ?)", (id, username)
        )

    def add_video(self, id: int, title: str, channel_id: int):
        self.conn.execute(
            "INSERT INTO videos(id, title, channel_id) VALUES(?, ?, ?)",
            (id, title, channel_id)
        )

    def add_comment(
        self,
        id: int,
        author_id: int,
        video_id: int,
        content: str,
        created_at: dt.datetime,
    ):
        self.conn.execute(
            "INSERT INTO comments VALUES(?, ?, ?, ?, ?)",
            (id, author_id, video_id, content, created_at),
        )

    def add_channel(self, id: int, name: str):
        self.conn.execute(
            "INSERT INTO channels(id, name) VALUES(?, ?)", (id, name)
        )

    def select(self, query: str):
        cursor = self.conn.execute(query)
        columns = next(zip(*cursor.description))
        return (columns, cursor.fetchall())
