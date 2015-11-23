#!/usr/bin/env python
# -*- coding: utf-8 -*--
from bs4 import BeautifulSoup
import urllib2
from urlparse import urljoin
import re


def scrape_type1(url):
  page = urllib2.urlopen(url)
  soup = BeautifulSoup(page.read(), 'html5lib')
  p = re.compile(r'\(.*\)')
  for a in soup.find_all("div", class_="mw-category")[0].find_all("a"):
    #print urljoin(url, a['href'])
    print p.sub('', a['title'])

def scrape_type2(url):
  page = urllib2.urlopen(url)
  soup = BeautifulSoup(page.read(), 'html5lib')
  p = re.compile(r'\(.*\)')
  for a in soup.find_all("div", class_="mw-content-ltr")[0].find_all("a", attrs = {'title' : True}):
    if not '.php' in a['href']:
      #print urljoin(url, a['href'])
      print p.sub('', a['title']), a.parent.contents[1]


if __name__ == "__main__":
  scrape_type1('https://en.wikipedia.org/wiki/Category:American_conceptual_artists')
  #scrape_type1('https://en.wikipedia.org/wiki/Category:Conceptual_artists')
  #scrape_type2('https://en.wikipedia.org/wiki/List_of_contemporary_artists')
