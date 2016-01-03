# Hangouts Bot Plugins

A repo of plugins for [hangoutsbot](https://github.com/hangoutsbot/hangoutsbot/).

## directions.py

Ask the bot for directions to and from places, based on certain trigger words: _how_, _long_, _take_, _to_, _from_.

    - How long will it take to get from Sydney to Canberra?
    - How long will it take to cycle from Sydney to Canberra?
    - How long will it take to walk from Sydney to Canberra?
    - How long will it take to get from Sydney to Canberra by public transport?

You'll need to add a **maps\_api\_key** with a maps API key. Also, it's currently biased towards Australia, because I'm lazy - I'll update the region bias to use a config parameter in the future.

### Requirements

- Google Maps Python library:

    pip3 install google-maps-services-python

- Textblob:

    pip3 install textblob
