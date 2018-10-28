#!/bin/false

import datetime

class date:
    def __init__(self, date):
        self.date = date
        self.str = date.strftime('%a %d %b')

        today = datetime.date.today()
        self.past = date < today
        self.today = date == today
        self.future = date > today

        if self.past:
            self.phase = 'past'
        elif self.today:
            self.phase = 'today'
        elif self.future:
            self.phase = 'future'
        else:
            raise Exception('invalid phase...')

    def __str__(self):
        return self.str

