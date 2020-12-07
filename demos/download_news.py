import requests
import json
import pandas as pd
from tqdm import tqdm
import time
import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], ".."))
from parler import Parler

# Returns domain names from affiliate news feed
def pageAffiliateFeed():
    dict1 = {}
    dict1["domain"] = []
    fetch = Parler().getAffiliateFeed()
    next_cursor = fetch["next"]
    # There are a lot of domains named "feedproxy.google.com", so I added a few lines to get the site if this is the domain
    for x in fetch["links"]:
        if x["domain"] != "feedproxy.google.com":
            dict1["domain"].append(x["domain"])
        elif x["domain"] == "feedproxy.google.com":
            dict1["domain"].append(x["metadata"]["site"])
    # Change "5" to a higher number to collect more posts
    for i in tqdm(range(1,5),desc="Collecting affiliate data..."):
        fetch = Parler().getAffiliateFeed(cursor=next_cursor)
        next_cursor = fetch["next"]
        for x in fetch["links"]:
            if x["domain"] != "feedproxy.google.com":
                dict1["domain"].append(x["domain"])
            elif x["domain"] == "feedproxy.google.com":
                 dict1["domain"].append(x["metadata"]["site"])
    df_affiliate_data = pd.DataFrame.from_dict(dict1)

    #Print 10 most frequent domains
    most_freq = pd.Series(' '.join(df_affiliate_data["domain"]).lower().split()).value_counts()[:10]
    print(most_freq)

pageAffiliateFeed()