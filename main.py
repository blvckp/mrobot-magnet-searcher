"""
    This program searches magnet links of episodes
    with 1080p (FHD) quality on "The Pirate Bay"!

    Author: blvckp
    Version: 0.3
"""

import requests
from BeautifulSoup import BeautifulSoup
import re

URL_BASE = 'https://thepiratebay.org/search/Mr.Robot.S02E'
URL_CATEGORY = '/0/99/200'

def get_content(episode = ''):

    print '\nPlease wait..\nGetting information..\n'
    req = requests.get(episode)

    if req.status_code == 200:
        result = str(req.content)
        if '<table id="searchResult">' in str(req.content):
            print 'Information received!\n'
            return result
        else:
            print 'Not found!'
            return False
    else:
        print 'Problem with request..\n'
        return False

def unquote(url):
  return re.compile('%([0-9a-fA-F]{2})',re.M).sub(lambda m: chr(int(m.group(1),16)), url)

def parse_content(content):
    soup = BeautifulSoup(content)
    filtered = str((soup.find('table', id='searchResult')))

    soup = BeautifulSoup(filtered)
    filtered = soup.findAll('a')

    for item in filtered:
        item = str(item)

        if '1080' in item and 'detLink' not in item:
            name = item[item.find('dn=')+3: item.find('tr=')-5].replace('+' , ' ').replace('.', ' ')
            print unquote(name) + ":"
            print " " + item[item.find('"') + 1:item.find("title") - 2] + "\n"

def check_input(string = ""):
    if string.isdigit():
        if int(string) < 10:
            return '0'+ string
        else:
            return string
    else:
        print 'Not correct input!\n'
        return False

if __name__ == "__main__":

    print "Which episode you are searching?\n"
    episode = ""

    while True:
        episode = check_input(raw_input("Episode #"))
        if episode is not False:
            break

    content = get_content(URL_BASE + episode + URL_CATEGORY)
    if content is not False:
        parse_content(str(content))
    else:
        exit()