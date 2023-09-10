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
                    title TEXT
                );
                CREATE TABLE IF NOT EXISTS comments (
                    id INTEGER PRIMARY KEY,
                    author_id INTEGER REFERENCES users(id),
                    video_id INTEGER REFERENCES videos(id),
                    content TEXT,
                    created_at DATETIME
                );
            """
            )
            yield cls(conn)

    def add_user(self, id: int, username: str):
        self.conn.execute("INSERT INTO users VALUES(?, ?)", (id, username))

    def add_video(self, id: int, title: str):
        self.conn.execute("INSERT INTO videos VALUES(?, ?)", (id, title))

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
