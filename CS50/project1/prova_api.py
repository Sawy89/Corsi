# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 15:51:32 2019
Try to access goodread api
Need a txt file with the key

@author: ddeen
"""

# Read KEY
f = open("goodreader.txt", "r")
d = {}
with open("goodreader.txt") as f:
    for line in f:
       (key, val) = line.replace('\n','').split(': ')
       d[key] = val

# try API
import requests
res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": d['key'], "isbns": "9781632168146"})
print(res.json())
