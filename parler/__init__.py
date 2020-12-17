import requests
import json
import time

class Parler:
    
    # Defines base URL and the cookie. Once you log into the app, paste your cookie here. 
    def __init__(self):
        self.base = "https://api.parler.com/v1"
        self.cookie = {"cookie": "mst=s%3AZYBOiM9xUTKauhOaElIYnTT63JTpxTphCJusxtyaOVdGjTCEkCDkNEIi3wonj3izIAIkPZPPg7yVv6pFSTX26ug3nEbAo2B7fikWpE2Km9DakydSfQbRiy65ouYIB1uH.XIGkDoMcgQEFAaWADMNWW0bLJtvwDlWWCByZamTvyaY; jst=eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJzZXNzaW9uSWQiOiIxNzYyOTk4NSIsInVzZXJJZCI6MTIwMjU1MTQsInBlcm1pc3Npb25zIjoyNTYsInZlcmlmaWVkIjpmYWxzZSwiaWF0IjoxNjA2OTQxNDk3LCJleHAiOjE2MDY5NDE3OTd9.4edDEiB_liniG8i4-Y-lRyDPndERXqGecx9AeoWdmDIQ1lKyrko4Z27h6WNEM8VLBkAjDDFjmFOX_N8sShCtEQ"}
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
    def getHashtags(self,q,limit=20,cursor=""):
        url = self.base + '/hashtag'
        params = (('search',q), ('limit',limit))
        if cursor != "":
            params = params + (("startkey",cursor),)
        response = requests.request("GET",url=url,headers=self.cookie,params=params)
        if self.handle_response(response).status_code != 200:
            print(f'Status: {response.status_code}')
            time.sleep(5)
            return self.getHashtags(q,limit,cursor)
        return response.json()
    
    # Returns list of posts containing a specified hashtag and metadata in JSON
    def getHashtagFeed(self,hashtag,limit=20,cursor=""):
        url = self.base + "/post/hashtag"
        headers = self.cookie
        params = (("tag",hashtag),("limit",limit))
        if cursor != "":
            params = params + (("startkey",cursor),)
        response = requests.request("GET",url=url,headers=headers,params=params)
        if self.handle_response(response).status_code != 200:
            print(f'Status: {response.status_code}')
            time.sleep(5)
            return self.getHashtagFeed(hashtag,limit,cursor)
        return response.json()
    
    # Returns list of posts from discover feed and metadata in JSON
    def getDiscoverFeed(self,limit=20,cursor=""):
        url = self.base + "/discover/posts"
        params = (("limit",limit))
        headers = self.cookie
        if cursor != "":
            params = params + (("startkey",cursor))
        response = requests.request("GET",url=url,headers=headers)
        if self.handle_response(response).status_code != 200:
            print(f'Status: {response.status_code}')
            time.sleep(5)
            return self.getDiscoverFeed(limit,cursor)
        return response.json()
    
    # Returns list of posts from affiliates and metadata in JSON
    def getAffiliateFeed(self,limit=20,cursor=""):
        params = (("limit",limit))
        headers = self.cookie
        url = self.base + '/discover/news'
        if cursor != "":
            params = params + (("startkey",cursor),)
        response = requests.get(url=url,headers=headers)
        if self.handle_response(response).status_code != 200:
            print(f'Status: {response.status_code}')
            time.sleep(5)
            return self.getAffiliateFeed(limit,cursor)
        return response.json()