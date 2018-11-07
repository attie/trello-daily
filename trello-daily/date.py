#!/bin/false

import datetime

class date:
    def __init__(self, date, today = None):
        self.date = date
        self.str = date.strftime('%a %d %b')
        self.list = None # list as-in trello list...
        self.pos = None # pos as-in trello position...

        if today is None:
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

    def __repr__(self):
        return '<trello-daily-date "%s">' % ( str(self) )

    def __eq__(self, other):
        if isinstance(other, str):
            return str(self) == other
        return super().__eq__(other)
