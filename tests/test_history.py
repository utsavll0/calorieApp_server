import datetime
import unittest
import os
import sys
# Get the current script's directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Get the parent directory
parent_dir = os.path.dirname(current_dir)

# Add the parent directory to the Python path
sys.path.append(parent_dir)
from service import history


class TestHistoryService(unittest.TestCase):

    def test_total_calories_to_burn_a(self):
        tw = 90
        cw = 100
        self.assertEqual(history.total_calories_to_burn(tw, cw), -77000)

    def test_total_calories_to_burn_b(self):
        tw = 100
        cw = 90
        self.assertEqual(history.total_calories_to_burn(tw, cw), 77000)

    def test_calories_to_burn_a(self):
        target_calories = -77000
        current_calories = 55500
        target_date = datetime.datetime.today() + datetime.timedelta(days=30 *
                                                                     11)
        start_date = datetime.datetime.today() - datetime.timedelta(days=30)
        val = history.calories_to_burn(target_calories, current_calories,
                                       target_date, start_date)
        self.assertAlmostEqual(val, -220)
