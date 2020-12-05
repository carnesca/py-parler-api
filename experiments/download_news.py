import requests
import json
import pandas as pd
from tqdm import tqdm
import time
from nltk.corpus import stopwords

#stopwords
stop = stopwords.words('english')
stop.extend(["still", "going", "like", "i", "the", "would", "get"])

def pageAffiliatedFeed():
    dict1 = {}
    dict1["domain"] = []
    df_affiliate_data = pd.DataFrame()
    fetch = Parler().getAffiliateFeed()
    next_cursor = fetch["next"]
    for x in fetch["links"]:
        if x["domain"] != "feedproxy.google.com":
            dict1["domain"].append(x["domain"])
        elif x["domain"] == "feedproxy.google.com":
            dict1["domain"].append(x["metadata"]["site"])
    for i in tqdm(range(1,3),desc="Collecting affiliate data..."):
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