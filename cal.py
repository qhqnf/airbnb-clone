from django.utils import timezone
import calendar


class Day:
    def __init__(self, number, past):
        self.number = number
        self.past = past

    def __str__(self):
        return str(self.number)


class Calender(calendar.Calendar):
    def __init__(self, year, month):
        super().__init__(firstweekday=6)
        self.year = year
        self.month = month
        self.months = [
            "January",
            "Febuary",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December",
        ]
        self.day_names = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]

    def get_month(self):
        return self.months[self.month - 1]

    def get_days(self):
        weeks = self.monthdays2calendar(self.year, self.month)
        days = []
        for week in weeks:
            for day, _ in week:
                now = timezone.now()
                today = now.day
                new_day = Day(day, day < today)
                days.append(new_day)
        return days
