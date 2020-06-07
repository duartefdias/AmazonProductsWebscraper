import requests
from bs4 import BeautifulSoup

## regex
import re

class Scraper:
    def __init__(self, searchTerm, pageNumber):
        self.currentPage = pageNumber
        self.searchTerm = searchTerm.replace(' ', '+')
        
        ## Need to add headers in requests or else amazon will give 503 erro (bot protection)
        ## Info on this: https://www.reddit.com/r/learnpython/comments/4eaz7v/error_503_when_trying_to_get_info_off_amazon/
        self.headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}


    def getItemLinksInPage(self):
        itemsUrls = []
        ## Make URL of search results
        URL = 'https://www.amazon.com/' + self.searchTerm.replace(' ', '-') + '/s?k=' + self.searchTerm.replace(' ', '+') + '&page=' + str(self.currentPage)
        print(URL)
        dom = requests.get(URL, headers = self.headers).text
        soup = BeautifulSoup(dom)
        productDivs = soup.findAll("div", {"class": "a-section a-spacing-medium"})
        
        for productDiv in productDivs:
            child = productDiv.findAll("a", {"class": "a-link-normal a-text-normal"}, href = True)
            print(child)
            if child:
                itemsUrls.append(productDiv.findChildren("a", {"class": "a-link-normal a-text-normal"}))


        ## Test html page result
        with open('search.html', 'w') as f:
            print(soup.encode('utf-8'), file=f)

        return itemsUrls


jarvis = Scraper('weird stuff', 2)
print(jarvis.getItemLinksInPage())