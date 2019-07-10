#!/usr/bin/python

import requests
import feedparser
import time
from subprocess import check_output
import sys
from bs4 import BeautifulSoup
import spacy

feed_name = 'BBC News'
url = 'http://feeds.bbci.co.uk/news/england/london/rss.xml'
db = 'feed_results.txt'
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

    nlp = spacy.load("en_core_web_sm")
    print(feed.entries)
    for post in feed.entries:
        link = post.id
        title = post.title
        save =  [link,title]
        if post_is_in_db_with_old_timestamp(link):
            posts_to_skip.append(save)
        else:
            posts_to_scrape.append(save)
    print(posts_to_scrape)
    output = []
    for item in posts_to_scrape:
        story = {}
        page = requests.get(item[0])
        soup = BeautifulSoup(page.text, 'html.parser')
        news_text = soup.find_all('p')
        text = ''
        for x in news_text: 
            x = str(x)
            s = x.find('>')
            y = x[s+1:]
            s = y.find('</')
            z = y[:s]
            print(z)
            text = text + z

        story['title'] = item[1]
        lp = spacy.load("en_core_web_sm")
        loc_url = "https://nominatim.openstreetmap.org/search?q="
        doc = nlp(text)
        print(doc.ents)
        for ent in doc.ents:
            if ent.label_ == 'location':
                getlatlon = locurl + ent.text
                response = requests.get(getlatlon)
                data = response.json()
                x = data.find('lat')
                dat =  data[x+7:]
                y = dat.find("'")
                lat = dat[:y+1]
                x = data.find('lon')
                dat =  data[x+7:]
                y = dat.find("'")
                lon = dat[:y+1]
                story['ent'] = ent,text, ent.label_
                story['ent']['lat'] = lat
                story['ent']['lon'] = lon                
            else:
                story['ent'] = ent.text, ent.label_
            output.append(story)
    out = open('output.json', 'w')
    out.write(str(output))

if __name__ == '__main__':
    main()
