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
        self.update_temporal_cards(board, dates)

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
            l = [ _ for _ in lists if _.name == date.str ]
            if len(l) == 1:
                date.list = l[0]
                continue
            elif len(l) > 1:
                raise Exception('multiple matching lists...')

            print('Create List [%s]...' % date.str )
            date.list = board.add_list(date.str)

    def order_lists(self, board, fallback_list, dates):
        lists = board.open_lists()
        for i, date in [ ( i + 2, _ ) for i, _ in enumerate(sorted(dates, key=lambda d: d.date)) ]:
            for l in [ _ for _ in lists if _.name == date.str ]:
                if l.pos == i:
                    continue

                print('Re-Ordering List [%s]... (%.3f -> %.3f)' % ( date.str, l.pos, i) )
                l.move(i)

        fallback_list.fetch()
        if fallback_list.pos != 1:
            print('Re-Ordering Fallback List... (%.3f -> %.3f)' % ( fallback_list.pos, 1 ))
            fallback_list.move(1)

    def update_temporal_cards(self, board, dates):
        board_labels = board.get_labels()

        temporal_labels = {}
        for phase in [ 'past', 'today', 'future' ]:
            label_id = oracle['daily']['%s_label_id' % ( phase )]
            temporal_labels[phase] = {
                'label_id': label_id,
                'label': next(filter(lambda _: _.id == label_id, board_labels))
            }

        for d in dates:
            temporal_cards = [ *self.get_cards_by_label(d.list, [ _['label'] for _ in temporal_labels.values() ]) ]

            if len(temporal_cards) == 0:
                # make new
                print('Creating Temporal Card for [%s]...' % ( d.str ))
                card = d.list.add_card('...')
            else:
                # update
                card = temporal_cards[0]

                # remove extra
                for rmcard in temporal_cards[1:]:
                    print('Removing Extra Temporal Card for [%s]...' % ( d.str ))
                    rmcard.delete()

            card.set_pos('top')

            if card.name != d.phase:
                card.set_name(d.phase)

            desired_label = temporal_labels[d.phase]

            needs_label = True
            for label in card.labels or []:
                if label.id == desired_label['label_id']:
                    needs_label = False
                    continue
                print('Removing Temporal Label from [%s]...' % ( d.str ))
                card.remove_label(label)

            if needs_label:
                print('Adding Temporal Label to [%s]...' % ( d.str ))
                card.add_label(desired_label['label'])

    def get_cards_by_label(self, lst, labels):
        yield from [ card for card in lst.list_cards() if self.card_has_one_of_labels(card, labels) ]

    def card_has_one_of_labels(self, card, labels):
        card_label_ids = [ _.id for _ in card.labels or [] ]
        label_ids = [ _.id for _ in labels or [] ]
        common = set(card_label_ids).intersection(label_ids)
        return len(common) > 0

    def get_date_range(self):
        date_now   = datetime.date.today()
        date_start = date_now - datetime.timedelta(days = oracle['daily']['days_past'])
        date_end   = date_now + datetime.timedelta(days = oracle['daily']['days_future'])
        date_span  = (date_end - date_start).days + 1 # +1 because we want today too

        for date in [ date_start + datetime.timedelta(days = _) for _ in range(0, date_span) ]:
            yield td_date(date, today = date_now)
