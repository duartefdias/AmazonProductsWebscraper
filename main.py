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


    # Working
    # Gets links of all product in the page
    def getItemLinksInPage(self):
        itemsUrls = []
        ## Make URL of search results
        URL = 'https://www.amazon.com/' + self.searchTerm.replace(' ', '-') + '/s?k=' + self.searchTerm.replace(' ', '+') + '&page=' + str(self.currentPage)
        # Get page DOM
        dom = requests.get(URL, headers = self.headers).text
        soup = BeautifulSoup(dom)
        
        # Get all product's outer div
        productDivs = soup.findAll("div", {"class": "a-section a-spacing-medium"})
        
        # Get each product's <a> tag and its respective href
        for productDiv in productDivs:
            child = productDiv.findAll("a", {"class": "a-link-normal a-text-normal"}, href = True)
            if child:
                for subChild in child:
                    itemsUrls.append('https://www.amazon.com' + subChild['href'])

        # Return list of product urls
        return itemsUrls

    def getProductInfo(self, url):
        '''
        Todo
        '''

    def addToDatabase(self):
        '''
        Todo
        '''

jarvis = Scraper('weird stuff', 2)
print(jarvis.getItemLinksInPage())