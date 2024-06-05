from app import db, create_app

app = create_app()
with app.app_context():
    db.create_all()
import sqlite3

conn = sqlite3.connect('food_data.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS foods (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    calories_per_unit REAL NOT NULL,
    kcal_per_unit REAL NOT NULL
)
''')

# Add some initial food data
foods = [
    ('Apple', 52, 52),
    ('Banana', 89, 89),
    ('Broccoli', 55, 55)
    # Add more food items here
]

cursor.executemany('''
INSERT INTO foods (name, calories_per_unit, kcal_per_unit) VALUES (?, ?, ?)
''', foods)

conn.commit()
conn.close()
