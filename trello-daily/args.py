#!/bin/false

import argparse

class Args:
    def __init__(self):
        self.argp = argparse.ArgumentParser(description = 'trello-daily todo list management')

        self.argp.add_argument('--config', help='the configuration file to use', default='./config.json')

        self.args = self.argp.parse_args()

args = Args().args

