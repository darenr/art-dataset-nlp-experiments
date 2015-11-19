from bs4 import BeautifulSoup
import urllib2
from urlparse import urljoin
import re


def scrape(url):
  page = urllib2.urlopen(url)
  soup = BeautifulSoup(page.read(), 'html5lib')
  p = re.compile(r'\(.*\)')
  for a in soup.find_all("div", class_="mw-category")[0].find_all("a"):
    #print urljoin(url, a['href'])
    print p.sub('', a['title'])


if __name__ == "__main__":
  scrape('https://en.wikipedia.org/wiki/Category:Conceptual_artists')
