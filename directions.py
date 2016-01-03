import logging
import hangups
import plugins
import asyncio

import googlemaps

logger = logging.getLogger(__name__)

from textblob import TextBlob
from urllib.parse import quote

def _initialise(bot):
    plugins.register_handler(_handle_message, type="message")

def _handle_message(bot, event, command):
    if isinstance(event.conv_event, hangups.ChatMessageEvent):
        event_type = "MESSAGE"
    elif isinstance(event.conv_event, hangups.MembershipChangeEvent):
        if event.conv_event.type_ == hangups.MembershipChangeType.JOIN:
            event_type = "JOIN"
        else:
            event_type = "LEAVE"
    elif isinstance(event.conv_event, hangups.RenameEvent):
        event_type = "RENAME"
    else:
        raise RuntimeError("unhandled event type")

    raw_text = " ".join(event.text.split())
    directions = ["how", "long", "take", "to", "from"]
    if all(x in raw_text.lower() for x in directions):
        yield from _getdirections(bot, event, raw_text, directions)

@asyncio.coroutine
def _getdirections(bot, event, text, type):
    logger.info("Directions from text: " + text)
    mapskey = bot.get_config_option("maps_api_key")
    if not mapskey.startswith("AIza"):
        return
    bicycling = ["by bicycling", "by cycling", "by bike", "a bicycle", "to cycle"]
    walking = ["on foot", "by walking", "to walk", "by foot"]
    transit = ["by public transport"]

    routeMode = ""

    if any(x in text for x in transit):
        routeMode = "transit"
        text = text.replace("by public transport", "")
    elif any(x in text for x in bicycling):
        routeMode = "bicycling"
    elif any(x in text for x in walking):
        routeMode = "walking"

    text = TextBlob(text)
    for s in text.sentences:
        logger.info(s)
        if all(x in s.lower() for x in type):
            dFrom = s.lower().words.index(type[-1])
            dTo = [i for i, x in enumerate(s.lower().words) if x == type[-2]][-1]
          
            if dFrom + 1 < dTo:
                origin = " ".join(s.words[dFrom + 1:dTo])
                destination = " ".join(s.words[dTo + 1:])
            elif dTo + 1 < dFrom:
                destination = " ".join(s.words[dTo + 1:dFrom])
                origin = " ".join(s.words[dFrom + 1:])

            gmaps = googlemaps.Client(key=mapskey)

            logger.info("origin: " + origin + "; destination: " + destination)

            if routeMode:
                dirs = gmaps.directions(origin, destination, mode=routeMode, region="au")
                logger.info("Distance mode: " + routeMode)
            else:
                dirs = gmaps.directions(origin, destination, region="au")
                logger.info("Distance mode: driving")
            try:
                dirs1 = dirs[0]
                dirlegs = dirs1["legs"]
                dirleg = dirlegs[0]
                duration = dirleg["duration"]
                time = duration["text"]
                startAddr = dirleg["start_address"]
                endAddr = dirleg["end_address"]
                logger.info("origin: " + origin + "/" + startAddr)
                logger.info("destination: " + destination + "/" + endAddr)
                mapsUrl = "https://www.google.com/maps?f=d&saddr=" + quote(startAddr) + "&daddr=" + quote(endAddr)
                routeUrlParams = {"walking":"w","transit":"r","bicycling":"b"}
                if routeMode: mapsUrl = mapsUrl + "&dirflg=" + routeUrlParams[routeMode]
                yield from bot.coro_send_message(event.conv, "Looks like it'll take you " + time + " to get from " + startAddr + " to " + endAddr + '. [<a href="' + mapsUrl + '" >maps</a>]')
            except IndexError:
                logger.error(dirs)

