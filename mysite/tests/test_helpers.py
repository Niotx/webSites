# tests/test_helpers.py
import unittest
from app.helpers import calculate_calories, calculate_bmi, convert_energy

class TestHelpers(unittest.TestCase):
    def test_calculate_calories(self):
        result = calculate_calories('Apple', 2)
        self.assertEqual(result, 104)

    def test_calculate_bmi(self):
        result = calculate_bmi(180, 75)
        self.assertAlmostEqual(result, 23.15, places=2)

    def test_convert_energy(self):
        kcal, kj = convert_energy('Banana', 2)
        self.assertEqual(kcal, 178)
        self.assertAlmostEqual(kj, 744.992, places=2)

if __name__ == '__main__':
    unittest.main()
