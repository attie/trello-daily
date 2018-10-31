#!/bin/false

import datetime
from trello import TrelloClient

from trello_daily.config import oracle
from trello_daily.date import date as td_date

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
        self.validate_temporal_labels(board)
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

    def validate_temporal_labels(self, board):
        label_ids = [ _.id for _ in board.get_labels() ]

        for key in [
            'past_label_id',
            'today_label_id',
            'future_label_id',
        ]:
            if oracle['daily'][key] not in label_ids:
                raise Exception('temporal label is missing...')

    def close_old_lists(self, board, fallback_list, dates):
        for l in board.open_lists():
            if l.id == oracle['daily']['fallback_list_id']:
                continue

            if l.name in [ _.str for _ in dates ]:
                continue

            print('Archive List [%s]...' % l.name )
            l.move_all_cards(fallback_list)
            l.close()

    def create_new_lists(self, board, dates):
        lists = board.open_lists()
        for date in dates:
            if date.str in [ _.name for _ in lists ]:
                continue

            print('Create List [%s]...' % date_str )
            board.add_list(date_str)

    def order_lists(self, board, fallback_list, dates):
        lists = board.open_lists()
        for i, date in [ ( i + 2, _ ) for i, _ in enumerate(sorted(dates, key=lambda d: d.date)) ]:
            for l in [ _ for _ in lists if _.name == date.str ]:
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
            yield td_date(date)
