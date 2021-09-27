import requests
import re
from bs4 import BeautifulSoup as bs
from _overlapped import NULL

#===============================================================================
# This function checks if a given book URL is listed within the robots.txt file of GoodReads.com.
# Returns true if there is a URL given that matches a line in the robots.txt but returns false otherwise.
#===============================================================================
def urlInRobotsFile(URL):
    f = open('robots.txt', 'r')
    while True:
        fp = f.readline()
        if (fp == ""):
            f.close()
            return False
        if ('/book/show/' in fp):
            x = fp.split('/')
            if (x[3].strip() in URL):
                f.close()
                return True
    

#===============================================================================
# Function that handles parsing and scraping a book page from a generic GoodReads.com Book page.
# Returns all the necessary values required for data storage.
#===============================================================================
def scrapeBookPage(URL):
    book_url = URL;
    request = requests.get(URL)
    soup = bs(request.text, 'html.parser')
    title = soup.find('h1', id='bookTitle').string.strip()
    book_id = soup.find('input', id='book_id')['value']
    if (soup.find('span', itemprop='isbn').string == NULL):
        ISBN = "does not exist"
    ISBN = soup.find('span', itemprop='isbn').string
    author_url = soup.find('a', class_='authorName')['href']
    author = soup.find('span', itemprop='name').string
    rating = soup.find('span', itemprop='ratingValue').string.strip()
    rating_count = soup.find('meta', itemprop='ratingCount')['content']
    review_count = soup.find('meta', itemprop='reviewCount')['content']
    image_url = soup.find('img', id='coverImage')['src']
    temp = soup.findAll('li', class_='cover')
    similar_books = []
    for b in temp:
        for child in b.find_all('a'):
            similar_books.append(child['href'])
    return book_url, title, book_id, ISBN, author_url, author, rating, rating_count, review_count, image_url, similar_books

#===============================================================================
# Function that handles parsing and scraping an author page from a generic GoodReads.com author page.
# Returns all the necessary values required for data storage.
#===============================================================================
def scrapeAuthorPage(URL):
    request = requests.get(URL)
    soup = bs(request.text, 'html.parser')
    name = soup.find('span', itemprop='name').string
    author_url = URL
    author_id = re.findall("\d+", URL)[0]
    rating = soup.find('span', itemprop='ratingValue').string
    rating_count = soup.find('span', class_="value-title")['title']
    review_count = soup.find('span', class_='count').find('span')['title']
    image_url = soup.find('div', class_='leftContainer authorLeftContainer').find('img')['src']
    tmp = soup.find('div', class_='hreview-aggregate').findAll('a')[1]['href']
    inp = 'http://goodreads.com'
    inp += tmp
    request2 = requests.get(inp)
    soup2 = bs(request2.text, 'html.parser')
    related_authors = []
    authorsURLs = soup2.findAll('a', class_="gr-h3 gr-h3--serif gr-h3--noMargin")
    for x in authorsURLs:
        related_authors.append(x['href'])
    temp = soup.findAll('td', width ='5%')
    author_books = []
    for b in temp:
        for child in b.findAll('a'):
            author_books.append(child['href'])
    return name, author_url, author_id, rating, rating_count, review_count, image_url, related_authors, author_books 
    
#===============================================================================
# Main call used for testing purposes.
#
# 
# def main():
#   
#     saveBookUrls = []
#     saveAuthorUrls = []
#     URL = 'https://www.goodreads.com/book/show/3735293-clean-code'
#     for x in range(4):
#         saveBookUrls.append(URL)
#         print('Begin scraping a page')
#         retArr = scrapeBookPage(URL)
#         print(retArr)
#         time.sleep(40)
#         URL = retArr[10][x]
#         for z in range(x):
#             if (URL == saveBookUrls[z]):
#                 URL = retArr[10][z+1]
#         print('Ended this scrape')
#         
#     URL = retArr[4]
#     for x in range(4):
#         saveAuthorUrls.append(URL)
#         print('Begin scraping a page')
#         retArr2 = scrapeAuthorPage(URL)
#         print(retArr2)
#         time.sleep(40) 
#         URL = retArr2[7][x]
#         for z in range(x+1):
#             if (URL == saveAuthorUrls[z]):
#                 URL = retArr2[7][z+1]   
#         print('Ended this scrape')
#         
#     
# if __name__ == "__main__":
#     main()
#===============================================================================