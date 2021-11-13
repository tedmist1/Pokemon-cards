import os
import re
import sys
import yaml
import warnings
import importlib
import concurrent.futures
import time

from bs4 import BeautifulSoup
from utils import get_webcontent, AuctionSpecifications


MAX_WORKERS = 8

def items_from_links(concat_search_page, search_base, search_range, link_to_item):
    item_set = set()
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        url_requests = {executor.submit(get_webcontent, concat_search_page, search_base, i):i
                        for i in range(1, search_range+1)}

        for future_obj in concurrent.futures.as_completed(url_requests):
            webcontent = future_obj.result()
            for link in BeautifulSoup(webcontent, 'html.parser').find_all('a'):
                item = link_to_item(link.get('href'))
                if item is not None:
                    item_set.add(item)
    return item_set


def write_bids(all_items, concat_bid_page, item_bid_parser, save_dirs):
    #with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        #url_requests = {executor.submit(get_webcontent, concat_bid_page, item): item
        #                for item in all_items}

        #for future_obj in concurrent.futures.as_completed(url_requests):
    t = 0
    while t < len(all_items):
        item = all_items[t]
        bid_page = get_webcontent(concat_bid_page, item)
        bid_item = item_bid_parser(bid_page, item)
        if bid_item is None:
            time.sleep(1)
            continue

        t += 1
        if t % 50 == 0:
            print(f'{t} items processed')

        file_path = os.path.join(save_dirs[bid_item.is_complete], bid_item.filename)

        with open(file_path, 'w') as fhndl:
            fhndl.write(bid_item.parsed_string)


        # Don't need this since I'm looking for completed items
        # if bid_item.is_complete:
        #     prog_file = os.path.join(save_dirs[not bid_item.is_complete], bid_item.filename)
        #     try:
        #         os.remove(prog_file)
        #     except FileNotFoundError:
        #         warnings.warn('{item} completed auction with no progress file.')
        

def collect_and_update(auction_specs):
    
    # Writing results directory
    save_path = os.path.join(auction_specs.save_root, auction_specs.save_name)
    save_dirs = [os.path.join(save_path, status) for status in ['in_progress', 'complete']]
    for save_dir in save_dirs:
        os.makedirs(save_dir, exist_ok=True)

    
    # Load auction specific reader (user implemented)
    auction_reader = importlib.import_module(auction_specs.py_implementation)

    # Get in-progress items
    prog_items = auction_reader.files_to_itemset(os.listdir(save_dirs[0]))
    # Gather new items
    new_items = items_from_links(auction_reader.concat_search_page, 
                                 auction_specs.site_specific_search_root, 
                                 auction_specs.max_search_page, auction_reader.link_to_item)
    # Write all items
    all_items = new_items.union(prog_items)
    print('Ebay likes asking for verification, this step gets throttled.\nWill sleep between verifies')
    write_bids(list(all_items), auction_reader.concat_bid_page, auction_reader.item_bid_parser, save_dirs)


if __name__ == '__main__':
    with open(sys.argv[1], 'r') as stream:
            yaml_dict = yaml.safe_load(stream)
    collect_and_update(AuctionSpecifications(**yaml_dict))
