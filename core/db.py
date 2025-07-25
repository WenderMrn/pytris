import sqlite3

from core.types import Score

with sqlite3.connect("pytetris_database.db", check_same_thread=False) as conn:
    cursor = conn.cursor()

    class Db:
        def __init__(self):
            self.__create_tables()

        def __create_tables(self):
            cursor.execute(
                """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                score INTEGER
            )
            """
            )

        def try_save_score(self, name: str, score: int):
            cursor.execute(
                """
                INSERT INTO users (name, score)
                SELECT ?, ?
                WHERE (
                    (SELECT COUNT(*) FROM users) < 5
                    OR
                    ? > (
                        SELECT MIN(score) FROM (
                            SELECT score FROM users ORDER BY score DESC LIMIT 5
                        )
                    )
                )
                AND NOT EXISTS (
                    SELECT 1 FROM users WHERE name = ? AND score = ?
                )
            """,
                (name, score, score, name, score),
            )

            conn.commit()

        def get_all_scores(self) -> list[Score]:
            res = conn.execute(
                "SELECT name, score FROM users ORDER BY score DESC LIMIT 5;"
            )
            rows = res.fetchall()

            if not rows:
                return []

            scores = []

            for name, value in rows:

                scores.append(Score(name, value))

            return scores

        def close(self):
            conn.close()
