#!/usr/bin/python

import requests
import feedparser
import time
from subprocess import check_output
import sys
from bs4 import BeautifulSoup

feed_name = 'BBC News'
url = 'http://feeds.bbci.co.uk/news/england/london/rss.xml'

db = 'https://axabbcntl.s3.eu-west-2.amazonaws.com/feed_results.txt'
limit = 12 * 3600 * 1000

#
# function to get the current time
#
current_time = lambda: int(round(time.time() * 1000))
timestamp = current_time()

def post_is_in_db(title):
    with open(db, 'r') as database:
        for line in database:
            if title in line:
                return True
    return False

# return true if the title is in the database with a timestamp > limit
def post_is_in_db_with_old_timestamp(link):
    with open(db, 'r') as database:
        for line in database:
            if link in line:
                ts_as_string = line.split('|', 1)[1]
                ts = long(ts_as_string)
                if timestamp - ts > limit:
                    return True
    return False

def main():
    feed = feedparser.parse(url)
    posts_to_scrape = []
    posts_to_skip = []

    for post in feed.entries:
        # if post is already in the database, skip it
        # TODO check the time
        link = post.id
        if post_is_in_db_with_old_timestamp(link):
            posts_to_skip.append(link)
        else:
            posts_to_scrape.append(link)
    
    #
    # add all the posts we're going to print to the database with the current timestamp
    # (but only if they're not already in there)
    #
    f = open(db, 'a')
    for link in posts_to_print:
        if not post_is_in_db(link):
            f.write(link + "|" + str(timestamp) + "\n")
    f.close
    
    count = 1
    blockcount = 1
    for link in posts_to_scrape:
        page = requests.get(link)
        soup = BeautifulSoup(page.text, 'html.parser')
        news_text = soup.find_all('p')
        out = open(link+'.txt', 'w')
        for x in news_text:
            x = str(x)
            s = x.find('>')
            y = x[s+1:]
            z = y[:-4]
            out.write(z)
        out.close()


if __name__ == '__main__':
    main()
