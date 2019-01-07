#!/bin/false

from trello import TrelloClient

from trello_daily.config import oracle

trello_client = TrelloClient(
    api_key = oracle['auth']['api_key'],
    api_secret = oracle['auth']['api_secret'],
    token = None,
    token_secret = None,
)
