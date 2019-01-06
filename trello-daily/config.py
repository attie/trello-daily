#!/bin/false

from json import load as json_load
from trello_daily.args import args

class Config:
    def __init__(self, filename = './config.json'):
        self.filename = filename
        self.config = self.read_config()

    def read_config(self):
        with open(self.filename, 'r') as f:
            config = json_load(f)

        self.validate_config(config)

        return config

    def validate_config(self, config):
        pass

    # --- #

    def __getitem__(self, key):
        return self.config[key]

    def __setitem__(self, key, value):
        self.config[key] = value

    def __contains__(self, key):
        return key in self.config

oracle = Config(filename = args.config)
