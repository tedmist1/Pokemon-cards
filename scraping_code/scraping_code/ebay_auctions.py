import re

from utils import BidItem
from bs4 import BeautifulSoup


ITM_RE = re.compile(r'itm\/(\d*)')

HOME_ROOT = 'https://www.ebay.com'
PAGE_QUANT = '&_pgn='
BID_INDEX = '/bfl/viewbids/'

# /sch/i.html?_from=R40&_trksid=p2334524.m570.l1313&_nkw=pokemon+celebrations+lances+charizard+V+box+sealed&_sacat=0&LH_TitleDesc=0&rt=nc&_odkw=pokemon+celebrations+lances+charizard+sealed+box&_osacat=0&LH_Complete=1&LH_Sold=1
# /b/CCG-Sealed-Packs/183456?mag=1&_fsrp=0&rt=nc&Game=Pok%25C3%25A9mon%2520TCG&Set=Celebrations%253A%2520Classic%2520Collection&Language=English&_sacat=183456&LH_Sold=1

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
    #print(bid_page)
    html_parsed = BeautifulSoup(bid_page, 'html.parser')
   # print(html_parsed)
   # print("~~~~~~~~~~~~~")
    # Prints out the original html to look through
    # print(html_parsed)
   
    #status_messages = html_parsed.find_all('span', attrs={'class':'app-listing-status_message'})
    status_messages = html_parsed.find_all('svg', attrs={'class':'icon icon--attention-filled'})
    
    # print(status_messages)
    
    is_complete = 'This item has ended.' in [mess.attrs['aria-label'] for mess in status_messages]

    # print(is_complete)


    filename = item + '.csv'
    parsed_string = 'user,bid,time'
    #bids_html = html_parsed.find_all('tr', attrs={'class':'ui-component-table_tr_detailinfo'})
    bids_html = html_parsed.find_all('tr')

    bids_name_html = html_parsed.find_all("span")


    for bid_name_html in bids_name_html:
        bid_text = bid_name_html.text

        if "Pokemon" in bid_text:
            print(bid_text)



    #print(bids_name_html)

    # Last bid is the starting bid
    for bid_html in bids_html:
        bid_text = bid_html.text
        dollar_loc = bid_text.find('$')
        

        if "Highest Bidder" in bid_text:
            print(str(dollar_loc) + " " + bid_text)


        #print(bid_text)

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
