import requests
import re
import time
from bs4 import BeautifulSoup as bs
from _overlapped import NULL

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

def scrapeAuthorPage(URL):
    request = requests.get(URL)
    soup = bs(request.text, 'html.parser')
    name = soup.find('span', itemprop='name').string
    author_url = URL
    author_id = re.findall("\d+", URL)[0]
    rating = soup.find('span', itemprop='ratingValue').string
    rating_count = soup.find('span', class_="value-title")['title']
    review_count = soup.find('span', class_='count').find('span')['title']
    image_url = soup.find('div', class_='leftContainer authorLeftContainer').find('img')['alt']
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
    
def main():

    saveBookUrls = []
    saveAuthorUrls = []
    URL = 'https://www.goodreads.com/book/show/3735293-clean-code'
    for x in range(4):
        saveBookUrls.append(URL)
        print('Begin scraping a page')
        retArr = scrapeBookPage(URL)
        print(retArr)
        time.sleep(40)
        URL = retArr[10][x]
        for z in range(x):
            if (URL == saveBookUrls[z]):
                URL = retArr[10][z+1]
        print('Ended this scrape')
    URL = retArr[4]
    for x in range(4):
        saveAuthorUrls.append(URL)
        print('Begin scraping a page')
        retArr2 = scrapeAuthorPage(URL)
        print(retArr2)
        time.sleep(40) 
        URL = retArr2[7][x]
        for z in range(x+1):
            if (URL == saveAuthorUrls[z]):
                URL = retArr2[7][z+1]   
        print('Ended this scrape')
        
    
if __name__ == "__main__":
    main()