# test_database.py

from lib.database import Database

def test_create_all():
    db = Database()
    print("Database initialized and tables created if they didn't exist.")

if __name__ == "__main__":
    test_create_all()
