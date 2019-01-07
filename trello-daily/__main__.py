#!/bin/false

# this is quite a nasty hack, but it decouples our 'package' name
# from the name of the directory that we're stored in... yik
if __name__ == '__main__':
    if __package__ is None:
        raise Exception('Do not run this directly... use python -m <module> instead...')
    if not __package__ == 'trello_daily':
        import sys
        sys.modules['trello_daily'] = sys.modules.pop(__package__)
        __package__ = 'trello_daily'
# ---

if __name__ == '__main__':
    from trello_daily.args import args

    if args.mode in [ 'daily' ]:
        from trello_daily.daily import Daily
        x = Daily()
        x.run()

    elif args.mode in [ 'show_boards', 'show_lists', 'show_labels' ]:
        from trello_daily.show import Show
        x = Show()
        getattr(x, args.mode)()
