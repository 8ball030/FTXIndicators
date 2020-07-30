import json
from multiprocessing import Process, Queue

import CONFIG
from ftx.ftxClient import FTXHelper

CLIENT = FTXHelper(api_key=CONFIG.APIKEY,
                   api_secret=CONFIG.SECRET,
                   subaccount_name=CONFIG.SUBACCOUNT)

in_q = Queue()


def do_work(i):
    while in_q.qsize() > 0:
        market = in_q.get()
        print(f"Processing : {market}")
        df = CLIENT.collect_dataframe_market(market=market)
        df.to_csv(f"./data/{market.replace('/', '_')}.csv", index=False)
    print(f"Process {i} Done.")


# we load up our job q


def main():
    with open("defi_markets.json", "r") as f:
        markets = json.loads(f.read())["markets"]
    print(markets)
    [in_q.put(p) for p in markets]  # (i) for i in markets]
    do_work("main")
#     # we create our worker threads
#     processes = [Process(target=do_work, args=[p]) for p in range(24)]
#     # we start our threads
#     [p.start() for p in processes]
#     [p.join() for p in processes]


if __name__ == "__main__":
    main()
