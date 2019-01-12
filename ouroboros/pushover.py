import http.client, urllib
import logging
import requests

#conn = http.client.HTTPSConnection("api.pushover.net:443")
log = logging.getLogger(__name__)


def post(token, user, device, title, container):
    """POST pushover for notifications"""
    try:
        message = "Container <b>" + container + "</b> has been updated."
        r = requests.post("https://api.pushover.net/1/messages.json", data = {
            "html": 1,
            "token": token,
            "user": user,
            "device": device,
            "title": title,
            "message": message,
        })
        print(r.text)
        log.info(r.text)
    except(Exception) as e:
        log.error(e)
