#!/bin/false

import argparse

class Args:
    def __init__(self):
        self.argp = argparse.ArgumentParser(description = 'trello-daily todo list management')

        self.argp.add_argument('--config', help='the configuration file to use', default='./config.json')
        self.argp.add_argument('--mode',   help='the mode to run in',            default='daily',
            choices = [
                'daily',
                'show_boards',
                'show_lists',
                'show_labels',
            ])

        self.args = self.argp.parse_args()

args = Args().args

