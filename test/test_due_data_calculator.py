from unittest import TestCase
from due_date_calculator import DueDateCalculator
from freezegun import freeze_time
from datetime import datetime as dt
from datetime import timedelta
import config


class TestDueDateCalculator(TestCase):

    @freeze_time('2018-10-22 12:00:01')
    def setUp(self):
        self.calculator = DueDateCalculator(config=config)

    @freeze_time('2018-10-22 12:00:01')
    def test_instantiation_with_no_args(self):
        DueDateCalculator(config=config)

    @freeze_time('2018-10-20 12:00:01')
    def test_instantiation_fails_with_invalid_date(self):
        with self.assertRaises(ValueError):
            DueDateCalculator(dt.now(), config=config)

    @freeze_time('2018-10-22 12:00:01')
    def test_init_with_now_args_results_in_now_start(self):
        calculator = DueDateCalculator(config=config)
        self.assertEqual(calculator.submitted_date, dt.now())

    @freeze_time('2018-10-22 12:00:01')
    def test_correct_due_date_is_given_monday_super_happy_path(self):
        calculator = DueDateCalculator(config=config)
        self.assertEqual(calculator.due_date, dt.now() + timedelta(days=2))

    @freeze_time('2018-10-19 12:00:01')
    def test_calculator_handles_weekends_gracefully(self):
        calculator = DueDateCalculator(config=config)
        self.assertEqual(calculator.due_date, dt.now() + timedelta(days=4))

    @freeze_time('2018-10-20')
    def test_is_weekday(self):
        self.assertFalse(self.calculator.is_weekday(dt.now()), 'Saturday')
        self.assertFalse(self.calculator.is_weekday(dt.now() + timedelta(days=1)), 'Sunday')
        self.assertTrue(self.calculator.is_weekday(dt.now() + timedelta(days=2)), 'Monday')
        self.assertTrue(self.calculator.is_weekday(dt.now() + timedelta(days=3)) , 'Tuesday')
        self.assertTrue(self.calculator.is_weekday(dt.now() + timedelta(days=4)), 'Wednesday')
        self.assertTrue(self.calculator.is_weekday(dt.now() + timedelta(days=5)), 'Thursday')
        self.assertTrue(self.calculator.is_weekday(dt.now() + timedelta(days=6)), 'Friday')
        self.assertFalse(self.calculator.is_weekday(dt.now() + timedelta(days=7)), 'Saturday')

    @freeze_time('2018-10-21')
    def test_is_open_hours(self):
        self.assertFalse(self.calculator.is_open_hours(dt.now()), "Too early: Midnight")
        self.assertFalse(self.calculator.is_open_hours(dt.now() + timedelta(hours=6)), 'Too early: 6am')
        self.assertTrue(self.calculator.is_open_hours(dt.now() + timedelta(hours=10)), 'Open: 10am')
        self.assertTrue(self.calculator.is_open_hours(dt.now() + timedelta(hours=16, minutes=59)), 'Open: 5:59pm')
        self.assertFalse(self.calculator.is_open_hours(dt.now() + timedelta(hours=17)), 'Too late: 6pm')
        self.assertFalse(self.calculator.is_open_hours(dt.now() + timedelta(days=-2)), 'Closed: Sunday')

    @freeze_time('2018-10-21')
    def test_is_business_hours_on_weekend(self):
        self.assertFalse(self.calculator.is_business_hour(dt.now()), "Too early: Midnight")
        self.assertFalse(self.calculator.is_business_hour(dt.now() + timedelta(hours=6)), 'Too early: 6am')
        self.assertFalse(self.calculator.is_business_hour(dt.now() + timedelta(hours=10)), 'Open: 10am')
        self.assertFalse(self.calculator.is_business_hour(dt.now() + timedelta(hours=16, minutes=59)), 'Open: 5:59pm')
        self.assertFalse(self.calculator.is_business_hour(dt.now() + timedelta(hours=17)), 'Too late: 6pm')
        self.assertFalse(self.calculator.is_business_hour(dt.now() + timedelta(days=-2)), 'Closed: Sunday')

    @freeze_time('2018-10-22')
    def test_is_busines_hours_on_weekday(self):
        self.assertFalse(self.calculator.is_business_hour(dt.now()), "Too early: Midnight")
        self.assertFalse(self.calculator.is_business_hour(dt.now() + timedelta(hours=6)), 'Too early: 6am')
        self.assertTrue(self.calculator.is_business_hour(dt.now() + timedelta(hours=10)), 'Open: 10am')
        self.assertTrue(self.calculator.is_business_hour(dt.now() + timedelta(hours=16, minutes=59)), 'Open: 5:59pm')
        self.assertFalse(self.calculator.is_business_hour(dt.now() + timedelta(hours=17)), 'Too late: 6pm')
        self.assertFalse(self.calculator.is_business_hour(dt.now() + timedelta(days=-2)), 'Closed: Sunday')
