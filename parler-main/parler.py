import requests
import json
import pandas as pd
from tqdm import tqdm
import time

class Parler():
    
    def __init__(self):
        self.base = "https://api.parler.com/v1"
        self.cookie = {"paste-cookie-here"}
        self.reconnects = 0
        
    def handle_response(self,response):
        if self.reconnects >= 10:
            raise Exception ("Internal abort; 10 reconnect attempts")
        elif response.status_code >=400 and response.status_code <=428:
            raise Exception ({'status':response.status_code,'error':response.reason,'English': "Most likely unauthorized or no results"})
        elif response.status_code == 502:
            print('Bad gateway error, retry in 5 seconds')
            self.reconnects += 1
        elif response.status_code == 429:
            print('Too many requests, retry in 5 seconds')
            self.reconnects += 1
        else: 
            self.reconnects = 0
        return response
    
    def getHashtagFeed(self,hashtag,limit=20,cursor=""):
        url = self. base + "/post/hashtag"
        headers = cookie
        params = (("tag",hashtag),("limit",limit))
        if cursor != "":
            params = params + (("startkey",cursor),)
        response = requests.request("GET",url=url,headers=headers,params=params)
        if self.handle_response(response).status_code != 200:
            print(f'Status: {response.status_code}')
            sleep(5)
            return self.getHashtagFeed(hashtag,limit,cursor)
        return response.json()
    
    def getDiscoverFeed(self,limit=20,cursor=""):
        url = self.base + "/discover/posts"
        params = (("limit",limit))
        headers = self.cookie
        if cursor != "":
            params = params + (("startkey",cursor))
        response = requests.request("GET",url=url,headers=headers)
        if self.handle_response(response).status_code != 200:
            print(f'Status: {response.status_code}')
            sleep(5)
            return self.getDiscoverFeed(limit,cursor)
        return response.json()
    
    def getAffiliateFeed(self,limit=20,cursor=""):
        url = self.base + "/discover/news"
        params = (("limit",limit))
        headers = self.cookie
        if cursor != "":
            params = params + (("startkey",cursor))
        response = requests.request("GET",url=url,headers=headers)
        if self.handle_response(response).status_code != 200:
            print(f'Status: {response.status_code}')
            time.sleep(5)
            return self.getAffiliateFeed(limit,cursor)
        return response.json()
