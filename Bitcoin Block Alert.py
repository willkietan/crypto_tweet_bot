import pandas as pd
import requests
import json
from urllib import parse as urlparse
import urllib3
import csv
import time

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

#Login
apikey = "Ni1gzj8jQQPzeYbGZu7haEpFGSzFHQWs"
api_root = "https://api.whale-alert.io/v1/status?api_key=" + apikey
endpoint = api_root
response = requests.get(endpoint, auth=("27072ce01a43d2d10eeb9d5ead7e7ee6-us9", apikey))
response = requests.get(endpoint)
response

#generate current Unix
current_time = round(time.time())
current_time

min_value = 500000
start = current_time - 60
end = current_time

api_root = "https://api.whale-alert.io/v1/transactions?api_key=" + apikey

endpoint = api_root + "&min_value=" + str(min_value) + "&start=" + str(start) + "&end=" + str(end)
response = requests.get(endpoint)

def find_owners(response): #transaction is passed
    owner_from = ""
    owner_to = ""
    if response['from']['owner_type'] == 'unknown': 
        owner_from = "unknown wallet"
    else:
        owner_from = "#" + response['from']['owner'] 

    if response['to']['owner_type'] == 'unknown': 
        owner_to = "unknown wallet"
    else:
        owner_to = "#" + response['to']['owner'] 
    return owner_from, owner_to

def generate_tweet(response):
    owner_from = find_owners(response)[0]
    owner_to = find_owners(response)[1]
    tweet = str("{0:,}".format(int(round(response['amount'])))) +     " #" + str(response['symbol']).upper() +     " (" + str("{0:,}".format(int(round(response['amount_usd'])))) +     " USD) transferred from " + str(owner_from) +     " to " + str(owner_to)

    return tweet

import tweepy

def send_to_twitter(tweet):
    twitter_auth_keys = { 
        "consumer_key"        : "",
        "consumer_secret"     : "",
        "access_token"        : "",
        "access_token_secret" : ""
    }
 
    auth = tweepy.OAuthHandler(
            twitter_auth_keys['consumer_key'],
            twitter_auth_keys['consumer_secret']
            )
    auth.set_access_token(
            twitter_auth_keys['access_token'],
            twitter_auth_keys['access_token_secret']
            )
    api = tweepy.API(auth)
 
    tweet = tweet
    status = api.update_status(status=tweet)

def run_code():
    #generate current Unix
    current_time = round(time.time())
    current_time

    min_value = 500000
    start = current_time - 5
    end = current_time

    api_root = "https://api.whale-alert.io/v1/transactions?api_key=" + apikey

    endpoint = api_root + "&min_value=" + str(min_value) + "&start=" + str(start) + "&end=" + str(end)
    response = requests.get(endpoint)
    
    if response.json()['count'] == 0:
        print("no transactions")
    
    try:
        for x in range(0, response.json()['count']):
            if response.json()['count'] == 0:
                "no transactions"
            else:
                tweet = generate_tweet(response.json()['transactions'][x])
                print(tweet)
                send_to_twitter(tweet)
    except KeyError as error:
        print("usage limit reached")

run_code()

import threading, time

def foo():
    print(time.ctime())
    
WAIT_TIME_SECONDS = 5

ticker = threading.Event()
while not ticker.wait(WAIT_TIME_SECONDS):
    foo()
    run_code()