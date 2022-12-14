import psycopg2


class AnimeDB:
    def __init__(self):
        self.conn = psycopg2.connect(database="Anime", user="postgres", password="123123")

        with self.conn.cursor() as cursor:
            cursor.execute("CREATE TABLE IF NOT EXISTS Anime(id SERIAL PRIMARY KEY, title TEXT NOT NULL);")
            cursor.execute("CREATE TABLE IF NOT EXISTS Seasons(id SERIAL PRIMARY KEY, title TEXT NOT NULL, anime INT NOT NULL REFERENCES Anime(id));")
            cursor.execute("CREATE TABLE IF NOT EXISTS Series(num INT NOT NULL, title TEXT NOT NULL, url TEXT NOT NULL UNIQUE, season INT NOT NULL REFERENCES Seasons(id), PRIMARY KEY (num, season));")
            self.conn.commit()

    def add_anime(self, title: str) -> int:
        with self.conn.cursor() as cursor:
            cursor.execute("INSERT INTO Anime(title) VALUES(%s) RETURNING id", (title.lower(),))
            self.conn.commit()
            return cursor.fetchone()[0]

    def add_season(self, title: str, anime: int) -> int:
        with self.conn.cursor() as cursor:
            cursor.execute("INSERT INTO Seasons(title, anime) VALUES(%s, %s) RETURNING id", (title.lower(), anime))
            self.conn.commit()
            return cursor.fetchone()[0]

    def add_episode(self, num: int, title: str, url: str, season: int):
        with self.conn.cursor() as cursor:
            cursor.execute("INSERT INTO Series(num, title, url, season) VALUES(%s, %s, %s, %s)", (num, title.lower(), url, season))
            self.conn.commit()

    def get_anime(self, title: str) -> list:
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT * FROM Anime WHERE title LIKE %s", (f"%{title.lower()}%",))
            return cursor.fetchall()

    def get_seasons(self, anime: int) -> list:
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT * FROM Seasons WHERE anime = %s", (anime,))
            return cursor.fetchall()

    def get_series(self, season: int) -> list:
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT * FROM Series WHERE season = %s", (season,))
            return cursor.fetchall()


if __name__ == "__main__":
    db = AnimeDB()
    #print(db.add_anime("Наруто"))
    #print(db.get_anime("Наруто"))
    print(db.add_episode(1, "daas", "https://google.com", 1))
