#!/bin/false

from trello_daily.config import oracle
from trello_daily.trello_client import trello_client

class Show:
    def __init__(self):
        self.tclient = trello_client

    def _print(self, l):
        for x in l:
            print('%s: %s' % ( x.id, x.name ))

    def show_boards(self):
        boards = self.tclient.list_boards()
        self._print(boards)

    def show_lists(self):
        board = self.tclient.get_board(oracle['daily']['board_id'])
        lists = board.all_lists()
        self._print(lists)

    def show_labels(self):
        board = self.tclient.get_board(oracle['daily']['board_id'])
        labels = board.get_labels()
        self._print(labels)
