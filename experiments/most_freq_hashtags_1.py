import requests
import json
import pandas as pd
from tqdm import tqdm
import time
from nltk.corpus import stopwords

#stopwords
stop = stopwords.words('english')

#Retrieves all available data for specified hashtag
def pageHashtagFeed(hashtag):
    dict1 = {}
    dict1["id"] = []
    dict1["body"] = []
    df_hashtag_data = pd.DataFrame()
    print("Collecting data for #" + hashtag + "...")
    fetch = Parler().getHashtagFeed(hashtag)
    next_cursor = fetch["next"]
    for x in fetch["posts"]:
        dict1["id"].append(x["id"])
        dict1["body"].append(x["body"])
    while fetch["last"] == False:
        fetch = Parler().getHashtagFeed(hashtag,cursor=next_cursor)
        next_cursor = fetch["next"]
        for x in fetch["posts"]:
            dict1["id"].append(x["id"])
            dict1["body"].append(x["body"])
    df_hashtag_data = pd.DataFrame.from_dict(dict1)
    

    #Prints 10 most frequent words
    df_disc_data["body_no_stopwords"] = df_disc_data["body"].apply([lambda x: ' '.join([word for word in x.split() if word not in stop])])
    most_freq = pd.Series(' '.join(df_disc_data["body_no_stopwords"]).lower().strip().split()).value_counts()[:10]
    print(most_freq)
