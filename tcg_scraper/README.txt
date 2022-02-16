Run the scrape.py file to gather data from the web, and save it to output file "etb.txt" and then process it with process.py 
Scrape.py is still a rough wip, though gets the job done. Would like to adjust it to not have magic numbers and be more generally applicable.
process.py still needs some work to properly process. Planning on having it save to a csv, and likely building a graph with the data.

etb.txt contains raw data through late November 2021.

commands:

python scrape.py > etb.txt
python process.py