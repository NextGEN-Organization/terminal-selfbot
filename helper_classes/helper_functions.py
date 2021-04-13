import json
import base64

from threading import Thread
from concurrent.futures import Future


async def getSuperProp(useragent):
    if "Windows" in useragent:
        os = "Windows"
        osver = "10"
    elif "Linux" in useragent:
        os = "Linux"
        osver = "X11"
    else:
        os = "Apple"
        osver = "10_9_3"
    browser_version = ' '.join(useragent.split('/')[3:4]).split(' ')[0]

    headers = {
        "os": os,
        "browser": "Chrome",
        "device": "",
        "browser_user_agent": useragent,
        "browser_version": browser_version,
        "os_version": osver,
        "referrer": "",
        "referring_domain": "",
        "referrer_current": "",
        "referring_domain_current": "",
        "release_channel": "stable",
        "client_build_number": 75603,
        "client_event_source": None
    }

    return base64.b64encode(json.dumps(headers, separators=",:").encode()).decode()



def call_with_future(fn, future, args, kwargs):
    try:
        result = fn(*args, **kwargs)
        future.set_result(result)
    except Exception as exc:
        future.set_exception(exc)


def threaded(fn):
    def wrapper(*args, **kwargs):
        future = Future()
        Thread(target=call_with_future, args=(fn, future, args, kwargs)).start()
        return future
    return wrapper
