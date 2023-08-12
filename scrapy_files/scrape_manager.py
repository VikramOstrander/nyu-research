# ------------
# script for running healthgrades_spider
# refer to readme.txt for usage
# ------------

from subprocess import call
import time
import datetime



# -----VALUES TO EDIT-----
# the starting position in the url dataset
START = 0
# total number of urls processed - max 3006892
FINISH = 3006892
# ------------------------



# number of urls processed in each spider call
NUM_URLS = 1000
# number of seconds to wait between each spider call
SLEEP_TIME = 30

# ensure FINISH is not greater than the total number of urls
data_length = 3006892
if(FINISH > data_length):
    FINISH = data_length

# time total program runtime
start_time = time.time()

# execute the spider
for i in range(START, FINISH, NUM_URLS):

    # begin timing spider process
    t = time.time()

    # call the spider in a subprocess to execute NUM_URLS urls
    call(f"scrapy crawl healthgrades_spider -a start={i} -a num={NUM_URLS}", shell=True)

    # end timing the spider process and calculate total time elapsed
    t = time.time() - t
    cur_time = str(datetime.timedelta(seconds=round(time.time()-start_time+SLEEP_TIME)))

    # print update
    print("-"*41)
    print(f"\t\tprocessed {(i+NUM_URLS)-START} in {cur_time}\nprogress:    \t{i+NUM_URLS} out of {FINISH}\ncurrent rate:\t{t/NUM_URLS:.6f} seconds per url")
    print("-"*41)

    # wait for SLEEP_TIME
    if i+NUM_URLS == FINISH:
        continue
    time.sleep(SLEEP_TIME)
