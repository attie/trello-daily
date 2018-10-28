#!/bin/false

import datetime
from trello import TrelloClient

from trello_daily.config import oracle

class daily:
    def __init__(self):
        self.tclient = TrelloClient(
            api_key = oracle['auth']['api_key'],
            api_secret = oracle['auth']['api_secret'],
            token = None,
            token_secret = None,
        )

    def run(self):
        board = self.tclient.get_board(oracle['daily']['board_id'])
        dates = [ *self.get_date_range() ]

        fallback_list = self.validate_fallback_list(board)
        self.close_old_lists(board, fallback_list, dates)
        self.create_new_lists(board, dates)
        self.order_lists(board, fallback_list, dates)

    def validate_fallback_list(self, board):
        if oracle['daily']['fallback_list_id'] not in [ _.id for _ in board.all_lists() ]:
            raise Exception('fallback list is missing...')

        fallback_list = board.get_list(oracle['daily']['fallback_list_id'])

        if fallback_list.closed:
            print('Re-Open Fallback List...')
            fallback_list.open()

        return fallback_list

    def close_old_lists(self, board, fallback_list, dates):
        for l in board.open_lists():
            if l.id == oracle['daily']['fallback_list_id']:
                continue

            if l.name in [ _[1] for _ in dates ]:
                continue

            print('Archive List [%s]...' % l.name )
            l.move_all_cards(fallback_list)
            l.close()

    def create_new_lists(self, board, dates):
        lists = board.open_lists()
        for date, date_str, date_today in dates:
            if date_str in [ _.name for _ in lists ]:
                continue

            print('Create List [%s]...' % date_str )
            board.add_list(date_str)

    def order_lists(self, board, fallback_list, dates):
        lists = board.open_lists()
        for i, date, date_str, date_today in [ ( _ + 2, __[0], __[1], __[2] ) for _, __ in enumerate(sorted(dates, key=lambda d: d[0])) ]:
            for l in [ _ for _ in lists if _.name == date_str ]:
                if l.pos == i:
                    continue

                print('Re-Ordering List [%s]...' % date_str )
                l.move(i)

        if fallback_list.pos != 1:
            print('Re-Ordering Fallback List...')
            fallback_list.move(1)

    def get_date_range(self):
        date_now   = datetime.date.today()
        date_start = date_now - datetime.timedelta(days = oracle['daily']['days_past'])
        date_end   = date_now + datetime.timedelta(days = oracle['daily']['days_future'])
        date_span  = (date_end - date_start).days + 1 # +1 because we want today too
        for date in [ date_start + datetime.timedelta(days = _) for _ in range(0, date_span) ]:
            yield date, date.strftime('%a %d %b'), date == date_now
