import requests
import json
import pandas as pd
from tqdm import tqdm
import time
from nltk.corpus import stopwords

#stopwords
stop = stopwords.words('english')
stop.extend(["still", "going", "like", "i", "the", "would", "get"])

def pageDiscoverFeed():
    dict_disc = {}
    dict_disc["id"] = []
    dict_disc["body"] = []
    fetch = Parler().getDiscoverFeed(cursor="")
    next_cursor = fetch["next"]
    for x in tqdm(range(1,3),desc="Collecting discover feed data"):
        time.sleep(3600)
        fetch = Parler().getDiscoverFeed(cursor=next_cursor)
        next_cursor = fetch["next"]
        for x in fetch["posts"]:
            dict_disc["id"].append(x["id"])
            dict_disc["body"].append(x["body"])
    df_disc_data = pd.DataFrame.from_dict(dict_disc)
    
    #Prints 10 most frequent words
    df_disc_data["body_no_stopwords"] = df_disc_data["body"].apply([lambda x: ' '.join([word for word in x.split() if word not in stop and not word.startswith('#')])])
    most_freq = pd.Series(' '.join(df_disc_data["body_no_stopwords"]).lower().strip().split()).value_counts()[:10]
    print(most_freq)
