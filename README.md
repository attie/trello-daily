# trello-daily

This project aims to help maintain daily to do lists using [Trello](https://trello.com/).

## Dependencies

- `py-trello` - [src](https://github.com/sarumont/py-trello) | [docs](https://py-trello.readthedocs.io/en/latest/)

## Authorization

Navigate to [trello.com/app-key](https://trello.com/app-key):

1. Copy your Developer API key into `config.json`, replacing `${YOUR_API_KEY}`
2. Generate a "_token_" (aka "_api_secret_") by following the "_... manually generate a **token**_" link
    - You may want to chagne the `name` field of the query string to better identify your `trello-daily` instance...

## Usage

TBD

## To Do

- Label / highlight weekend lists
- Set due date of a card if it is on a day list
- Highlight Future / Today / Past lists
