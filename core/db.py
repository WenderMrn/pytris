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
                    name TEXT NOT NULL UNIQUE,
                    score INTEGER NOT NULL
                )
            """
            )

        def try_save_score(self, name: str, score: int):
            # Garante a inserção ou atualização
            cursor.execute(
                """
                INSERT INTO users (name, score)
                VALUES (?, ?)
                ON CONFLICT(name) DO UPDATE SET score = 
                    CASE 
                        WHEN excluded.score > users.score THEN excluded.score
                        ELSE users.score
                    END
                """,
                (name, score),
            )

            # Mantém apenas os 5 melhores scores
            cursor.execute(
                """
                DELETE FROM users
                WHERE name NOT IN (
                    SELECT name FROM users
                    ORDER BY score DESC
                    LIMIT 5
                )
                """
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
