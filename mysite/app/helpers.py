# helpers.py
import sqlite3

def calculate_calories(food_item, quantity):
    conn = sqlite3.connect('food_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT calories_per_unit FROM foods WHERE name=?", (food_item,))
    result = cursor.fetchone()
    if result:
        calories_per_unit = result[0]
        total_calories = calories_per_unit * quantity
        return total_calories
    else:
        return None

def calculate_bmi(height, weight):
    return weight / ((height / 100) ** 2)

def convert_energy(food_item, quantity):
    conn = sqlite3.connect('food_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT kcal_per_unit FROM foods WHERE name=?", (food_item,))
    result = cursor.fetchone()
    if result:
        kcal_per_unit = result[0]
        total_kcal = kcal_per_unit * quantity
        total_kj = total_kcal * 4.184
        return total_kcal, total_kj
    else:
        return None, None
