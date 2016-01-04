# Hangouts Bot Plugins

A repo of plugins for [hangoutsbot](https://github.com/hangoutsbot/hangoutsbot/).

## directions.py

Ask the bot for directions to and from places, based on certain trigger words: _how_, _long_, _take_, _to_, _from_.

- How long will it take to get from Sydney to Canberra?
- How long will it take to cycle from Sydney to Canberra?
- How long will it take to walk from Sydney to Canberra?
- How long will it take to get from Sydney to Canberra by public transport?

The bot will also send the user help if they send the `/bot directionshelp` command.

### Setup

1. Create a `maps_api_key` config parameter with a Google Maps API Key. If you need help getting an API key, [read the docs](https://developers.google.com/maps/documentation/directions/get-api-key) for help.

2. Create a `directions_geobias` config parameter with a Google Maps [ccTLD](https://en.wikipedia.org/wiki/Country_code_top-level_domain) of any country where Google Maps has launched dirving directions. See [the docs](https://developers.google.com/maps/documentation/directions/intro#RegionBiasing) for help.

### Requirements

- Google Maps Python library:

  `pip3 install google-maps-services-python`

- Textblob:

  `pip3 install textblob`

## Bugs, questions and feature requests

Submit an issue here on GitHub, or if you can fix the bug (or add a new feature) I assume you know what a pull request is ;)

