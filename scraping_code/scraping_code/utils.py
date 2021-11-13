import http
import urllib.request

from dataclasses import dataclass


@dataclass
class BidItem:
    filename: str
    is_complete: bool
    parsed_string: str


@dataclass
class AuctionSpecifications:
    save_root: str
    save_name: str
    py_implementation: str
    site_specific_search_root: str
    max_search_page: int


def get_webcontent(concat_webpage, *args):
    page_str = concat_webpage(*args)
    req = urllib.request.Request(page_str, headers={'User-Agent': 'Chrome'})
    url = urllib.request.urlopen(req)

    try:
        webcontent = url.read()
    except http.client.IncompleteRead:  # Catch partial reads and re-initiate
        webcontent = get_webcontent(concat_webpage, *args)

    return webcontent
