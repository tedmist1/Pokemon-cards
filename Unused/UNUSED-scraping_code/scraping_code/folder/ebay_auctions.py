import re

from utils import BidItem
from bs4 import BeautifulSoup


ITM_RE = re.compile(r'itm\/(\d*)')

HOME_ROOT = 'https://www.ebay.com'
PAGE_QUANT = '&_pgn='
BID_INDEX = '/bfl/viewbids/'


def concat_search_page(search_base, page_id):
    return HOME_ROOT + search_base + PAGE_QUANT + str(page_id)


def concat_bid_page(item):
    return HOME_ROOT + BID_INDEX + item


def files_to_itemset(filenames):
    return set([filename.split('.')[0] for filename in filenames])


def link_to_item(link):
    grp_list = ITM_RE.findall(link)
    if len(grp_list) == 1:
        return grp_list[0]
    elif len(grp_list) > 1:
        raise Exception(f'Multiple groups found in {link}.\nGroupings: {grp_list}')
    else:
        return None  # redundant but explicit


# Not easily generalizable. Most susceptible to changes.
def item_bid_parser(bid_page, item):
    html_parsed = BeautifulSoup(bid_page, 'html.parser')

    #status_messages = html_parsed.find_all('span', attrs={'class':'app-listing-status_message'})
    status_messages = html_parsed.find_all('svg', attrs={'class':'icon icon--attention-filled'})
    is_complete = 'This item has ended.' in [mess.attrs['aria-label'] for mess in status_messages]

    filename = item + '.csv'
    parsed_string = 'user,bid,time'
    #bids_html = html_parsed.find_all('tr', attrs={'class':'ui-component-table_tr_detailinfo'})
    bids_html = html_parsed.find_all('tr')

    # Last bid is the starting bid
    for bid_html in bids_html:
        bid_text = bid_html.text
        dollar_loc = bid_text.find('$')
        if dollar_loc != -1:
            # clean bid
            bid_text = bid_text.strip(' Highest Bidder ')

            # find place markers
            bid_subtext = bid_text[dollar_loc:]
            space_loc = bid_subtext.find(' ') + dollar_loc

            # get relevant info
            user = bid_text[:dollar_loc]
            bid = bid_text[dollar_loc:space_loc]
            time = bid_text[space_loc+1:]

            parsed_string += '\n' + ','.join([user,bid,time])

        #bid_line = '\n' + ','.join([bid_elem.text for bid_elem in bid_html.find_all('td')])
        #parsed_string += bid_line
    auc_info = html_parsed.find('div', attrs={'class':'app-bid-info-upgrade_wrapper'})
    if auc_info is None:  # round the day on bids
        return 
    parsed_string += '\n' + ','.join([el.text for el in auc_info.find_all('li')])

    return BidItem(filename=filename, is_complete=is_complete, parsed_string=parsed_string)
