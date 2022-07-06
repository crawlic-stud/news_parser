import sqlite3


class DatabaseCursor:
    def __init__(self, db_path):
        self.db_path = db_path
        self.connection = None

    def __enter__(self):
        self.connection = sqlite3.connect(self.db_path)
        return self.connection.cursor()

    def __exit__(self, exc_type, exc_value, exc_tb):
        # print(exc_type, exc_value, exc_tb)
        self.connection.commit()
        self.connection.close()


def execute(command, db_path="news.db"):
    with DatabaseCursor(db_path) as cursor:
        cursor.execute(command)
        return cursor.fetchall()
