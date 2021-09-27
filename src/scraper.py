"""
Implements the scraping of book and author data from GoodReads.com
"""
import re
import requests
from bs4 import BeautifulSoup as bs

def url_in_robots_file(url):
    """
    This function checks if a given book URL is listed within
    the robots.txt file of GoodReads.com.
    Returns true if there is a URL given that matches a line
    in the robots.txt but returns false otherwise.
    """
    file = open('robots.txt', 'r')
    while True:
        line = file.readline()
        if line == "":
            file.close()
            return False
        if '/book/show/' in line:
            parse = line.split('/')
            if parse[3].strip() in url:
                file.close()
                return True
def scrape_book_page(url):
    """
    Function that handles parsing and scraping a book page from a
    generic GoodReads.com Book page.
    Returns all the necessary values required for data storage.
    """
    book_url = url
    request = requests.get(url)
    soup = bs(request.text, 'html.parser')
    title = soup.find('h1', id='bookTitle').string.strip()
    book_id = soup.find('input', id='book_id')['value']
    if soup.find('span', itemprop='isbn').string is None:
        isbn = "does not exist"
    isbn = soup.find('span', itemprop='isbn').string
    author_url = soup.find('a', class_='authorName')['href']
    author = soup.find('span', itemprop='name').string
    rating = soup.find('span', itemprop='ratingValue').string.strip()
    rating_count = soup.find('meta', itemprop='ratingCount')['content']
    review_count = soup.find('meta', itemprop='reviewCount')['content']
    image_url = soup.find('img', id='coverImage')['src']
    temp = soup.findAll('li', class_='cover')
    similar_books = []
    for search in temp:
        for child in search.find_all('a'):
            similar_books.append(child['href'])
    return book_url, title, book_id, isbn, author_url, author, rating, rating_count, review_count, image_url, similar_books
def scrape_author_page(url):
    """
    Function that handles parsing and scraping an author page from
    a generic GoodReads.com author page.
    Returns all the necessary values required for data storage.
    """
    request = requests.get(url)
    soup = bs(request.text, 'html.parser')
    name = soup.find('span', itemprop='name').string
    author_url = url
    author_id = re.findall("\d+", url)[0]
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
    authors_urls = soup2.findAll('a', class_="gr-h3 gr-h3--serif gr-h3--noMargin")
    for authors in authors_urls:
        related_authors.append(authors['href'])
    temp = soup.findAll('td', width ='5%')
    author_books = []
    for search in temp:
        for child in search.findAll('a'):
            author_books.append(child['href'])
    return name, author_url, author_id, rating, rating_count, review_count, image_url, related_authors, author_books
