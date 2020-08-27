import requests
from bs4 import BeautifulSoup
import sys

from database import Database

class Scraper:
    def __init__(self, searchTerm, pageNumber):
        self.currentPage = pageNumber
        self.searchTerm = searchTerm.replace(' ', '+')
        
        ## Need to add headers in requests or else amazon will give 503 erro (bot protection)
        ## Info on this: https://www.reddit.com/r/learnpython/comments/4eaz7v/error_503_when_trying_to_get_info_off_amazon/
        self.headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}


    # Gets links of all product in the page
    def getItemLinksInPage(self):
        itemsUrls = []
        ## Make URL of search results
        URL = 'https://www.amazon.com/' + self.searchTerm.replace(' ', '-') + '/s?k=' + self.searchTerm.replace(' ', '+') + '&page=' + str(self.currentPage)
        print('\nSearch URL:\n' + URL + '\n')
        # Get page DOM
        dom = requests.get(URL, headers = self.headers).text
        soup = BeautifulSoup(dom, 'lxml')
        
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

    # Get info of an Amazon product given its url
    def getProductInfo(self, url):
        # Define product dictionary
        productInfo = {}
        productInfo['affiliateLink'] = url
        
        # Get page DOM
        dom = requests.get(url, headers = self.headers).text
        soup = BeautifulSoup(dom, 'lxml')

        # Get image source
        productImageDivs = soup.findAll("div", {"class": "imgTagWrapper"})
        productInfo['imageUrls'] = []

        for productDiv in productImageDivs:
            imgTag = productDiv.findAll("img")
            if imgTag:
                productInfo['imageUrls'].append(imgTag[0].attrs['data-old-hires'])

        if(productInfo['imageUrls']):
            productInfo['imageURL'] = productInfo['imageUrls'][0]

        # Get product title
        productInfo['title'] = ''
        productTitleSpans = soup.findAll("span", {"id": "productTitle"})
        if productTitleSpans is not None:
            if productTitleSpans:
                productInfo['title'] = productTitleSpans[0].text.strip()

        # Get product price
        productInfo['price'] = ''
        productPriceSpan = soup.find("span", {"id": "priceblock_ourprice"})
        if productPriceSpan is None:
            productPriceSpan = soup.find("span", {"id": "priceblock_saleprice"})
        if productPriceSpan is not None:
            # Remove currency sign
            productInfo['price'] = productPriceSpan.text.replace('$', '')
            # Remove additional clutter (example: '48.99 - 125.00')
            productInfo['price'] = productInfo['price'].split(' ')[0]
            # Convert string into float
            productInfo['price'] = float(productInfo['price'])

        # Get product description
        productInfo['description'] = ''
        productDescriptionDiv = soup.find("div", {"id": "productDescription"})
        if productDescriptionDiv is not None:
            productInfo['description'] = productDescriptionDiv.find("p").text.strip()

        return productInfo

def printItemInfo(item):
    print("Images in item: ", len(item['imageUrls']))
    print("Title: ", item['title'])
    print("Price: ", item['price'])
    if item['description']:
        print("Description: Yes\n")
    else:
        print("Description: No\n")

# Example execution: python .\main.py 'weird products' 30 1
# 30 -> Number of product to add
# 1 -> Starting result page
def main():
    searchTerm = sys.argv[1] #'weird stuff'
    numberOfProductsToAdd = int(sys.argv[2]) # 10
    startingResultsPage = int(sys.argv[3]) # Use 1 by default
    db = Database()

    remainingProductsInPage = 0
    currentPageItem = 0

    # Initialize Scraper object
    jarvis = Scraper(searchTerm, startingResultsPage)

    # Iterate through number of product to add
    while numberOfProductsToAdd > 0:
        # Check if there are still items in the page that weren't added to the db
        if remainingProductsInPage == 0:
            jarvis.currentPage = jarvis.currentPage + 1
            searchPageItemsUrls = jarvis.getItemLinksInPage()

        # Get info on a single product
        if(len(searchPageItemsUrls) == 0):
            return print('Amazon showing robot verification or invalid page, try again in a few minutes')
        print(searchPageItemsUrls[currentPageItem])
        itemInfo = jarvis.getProductInfo(searchPageItemsUrls[currentPageItem])
        printItemInfo(itemInfo)
        currentPageItem = currentPageItem + 1
        remainingProductsInPage = remainingProductsInPage - 1
        numberOfProductsToAdd = numberOfProductsToAdd - 1

        # Add product to database
        db.insertProduct(itemInfo)

if __name__ == "__main__":
    main()