import sqlite3
import sys
import default


def get_db(path: str):
    db = sqlite3.connect(path)
    db.row_factory = sqlite3.Row
    return db


if __name__ == "__main__":
    if sys.argv[1] == "reset":
        settings = default.Settings("settings.json")
        db = get_db(settings["database"])
        db.executescript("""
        DROP TABLE IF EXISTS groups;
        
        CREATE TABLE groups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            discord_id INTEGER UNIQUE NOT NULL,
            guild_id INTEGER NOT NULL,
            owner_id INTEGER NOT NULL
        )   ;     
        """)
        db.commit()
        db.close()