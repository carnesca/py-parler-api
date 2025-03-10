import requests
import json
import time

class Parler:
    
    # Defines base URL and the cookie. Once you log into the app, paste your cookie here. 
    def __init__(self):
        self.base = "https://api.parler.com/v1"
        self.cookie = {"cookie": "paste-cookie-here"}
        self.reconnects = 0
        
    # Handles HTTP responses
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

    # Returns list of hashtags containing specified term and total posts which contain that hashtag
    def hashtags(self,q,limit=20,cursor=""):
        url = self.base + '/hashtag'
        params = (('search',q), ('limit',limit))
        if cursor != "":
            params = params + (("startkey",cursor),)
        response = requests.request("GET",url=url,headers=self.cookie,params=params)
        if self.handle_response(response).status_code != 200:
            print(f'Status: {response.status_code}')
            time.sleep(5)
            return self.get_hashtags(q,limit,cursor)
        return response.json()
    
    # Returns list of posts containing a specified hashtag and metadata in JSON
    def hashtag_feed(self,hashtag,limit=20,cursor=""):
        url = self.base + "/post/hashtag"
        headers = self.cookie
        params = (("tag",hashtag),("limit",limit))
        if cursor != "":
            params = params + (("startkey",cursor),)
        response = requests.request("GET",url=url,headers=headers,params=params)
        if self.handle_response(response).status_code != 200:
            print(f'Status: {response.status_code}')
            time.sleep(5)
            return self.get_hashtag_feed(hashtag,limit,cursor)
        return response.json()
    
    # Returns list of posts from discover feed and metadata in JSON
    def discover(self,limit=20,cursor=""):
        url = self.base + "/discover/posts"
        params = (("limit",limit))
        headers = self.cookie
        if cursor != "":
            params = params + (("startkey",cursor))
        response = requests.request("GET",url=url,headers=headers)
        if self.handle_response(response).status_code != 200:
            print(f'Status: {response.status_code}')
            time.sleep(5)
            return self.discover(limit,cursor)
        return response.json()
    
    # Returns list of posts from affiliates and metadata in JSON
    def affiliates(self,limit=20,cursor=""):
        params = (("limit",limit))
        headers = self.cookie
        url = self.base + '/discover/news'
        if cursor != "":
            params = params + (("startkey",cursor),)
        response = requests.get(url=url,headers=headers)
        if self.handle_response(response).status_code != 200:
            print(f'Status: {response.status_code}')
            time.sleep(5)
            return self.affiliates(limit,cursor)
        return response.json()