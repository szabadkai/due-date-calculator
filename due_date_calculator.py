from datetime import datetime
from datetime import timedelta

import config


class DueDateCalculator:
    submitted_date: datetime

    def __init__(self, submitted=None, config=config):
        self.submitted_date = submitted if submitted is not None else datetime.now()
        self.ETA_HOURS = config.ETA_HOURS
        self.BUSINESS_HOURS_START = config.BUSINESS_HOURS_START
        self.BUSINESS_HOURS_DURATION = config.BUSINESS_HOURS_DURATION
        self.WEEKDAYS = config.WEEKDAYS
        if not self.is_business_hour(self.submitted_date):
            raise ValueError(f'Submission date {self.submitted_date} in out of working hours')

    @property
    def due_date(self):
        due_date = self.submitted_date

        for _ in range(self.ETA_HOURS):
            while True:
                due_date += timedelta(hours=1)
                if self.is_business_hour(due_date):
                    break

        return due_date

    def is_weekday(self, d: datetime):
        return d.weekday() in self.WEEKDAYS

    def is_open_hours(self, d):
        return self.BUSINESS_HOURS_START <= d.hour and d.hour < self.BUSINESS_HOURS_START + self.BUSINESS_HOURS_DURATION

    def is_business_hour(self, d: datetime):
        return self.is_weekday(d) and self.is_open_hours(d)

    def CalculateDueDate(self):
        return self.due_date
