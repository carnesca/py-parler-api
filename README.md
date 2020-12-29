# Python Interface for Parler API

## About

This library is designed to easily programatically fetch data from the social media site Parler. The latest version can:

* Download posts which contain a specified hashtag
* Download posts from the discover feed
* Download metadata/posts from the affiliate's feed

## How To:

### Authentication

Parler.com requires both a CAPTCHA solution and an SMS verification code every time a user logs in. Therefore, you will need to first log into the platform in your browser, go through the CAPTCHA and SMS verifcation and use Inspect > Network > Headers > Request Headers to retrieve the cookie that was created in order to make requests with this repo. You'll want to copy the entire cookie: 

![Parler](/screenshots/parler_screenshot.png)

The cookie should be pasted here in the parler-main/parler.py file:

![Parler.py](/screenshots/parler_screenshot_2.jpg)

## Demo

I've written some examples of how the functions can be used [here](demo_parler.ipynb)

### *Note*: 
*Parler's API is not meant to be public-facing nor optimized for programatic use. Because of this, you can currently only retrieve up to 20 posts at a time. Therefore, any large amount of data will take a long time to retrieve.*  
  
  
 ## Disclaimer
 
 I am in no way affiliated with Parler.com or any entity related to Parler.com. I am not responsible for what you do with this repository. 