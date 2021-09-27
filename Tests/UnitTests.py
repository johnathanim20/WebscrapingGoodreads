'''
Created on Sep 26, 2021

@author: johna
'''
import unittest
import time
from Scraper import scrapeBookPage
from Scraper import scrapeAuthorPage
from Scraper import urlInRobotsFile
from CommandLine import checkIfAuthor
from CommandLine import checkIfBook

class Test(unittest.TestCase):
    
    def test_UrlInRobotsFile(self):
        URL = 'https://www.goodreads.com/book/show/52976360-coronavirus-and-christ'
        flag = urlInRobotsFile(URL)
        self.assertEqual(flag, True)
    
    def test_UrlInRobotsFile2(self):
        URL = 'https://www.goodreads.com/book/show/3735293-clean-code'
        flag = urlInRobotsFile(URL)
        self.assertEqual(flag, False)
        
    def test_ScrapeBookPage(self):
        URL = 'https://www.goodreads.com/book/show/3735293-clean-code'
        retArr = scrapeBookPage(URL)
        self.assertEqual(retArr[0], 'https://www.goodreads.com/book/show/3735293-clean-code')
        self.assertEqual(retArr[1], 'Clean Code: A Handbook of Agile Software Craftsmanship')
        self.assertEqual(retArr[2], '3735293')
        self.assertEqual(retArr[3], '9780132350884')
        self.assertEqual(retArr[4], 'https://www.goodreads.com/author/show/45372.Robert_C_Martin')
        self.assertEqual(retArr[5], 'Robert C. Martin')
        #self.assertEqual(retArr[6], '4.40')
        #self.assertEqual(retArr[7], '17127')
        #self.assertEqual(retArr[8], '1030')
        self.assertEqual(retArr[9], 'https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1436202607l/3735293._SX318_.jpg')
        time.sleep(40)
        
    def test_ScrapeBookPage2(self):
        URL = 'https://www.goodreads.com/author/show/45372.Robert_C_Martin'
        try:
            retArr = scrapeBookPage(URL)
        except:
            retArr = None
        self.assertEqual(retArr, None)

        
    def test_ScrapeAuthorPage(self):
        URL = 'https://www.goodreads.com/author/show/45372.Robert_C_Martin'
        retArr = scrapeAuthorPage(URL)
        self.assertEqual(retArr[0], 'Robert C. Martin')
        self.assertEqual(retArr[1], 'https://www.goodreads.com/author/show/45372.Robert_C_Martin')
        self.assertEqual(retArr[2], '45372')
        #self.assertEqual(retArr[3], '4.34')
        #self.assertEqual(retArr[4], '31522')
        #self.assertEqual(retArr[5], '2093')
        self.assertEqual(retArr[6], 'https://images.gr-assets.com/authors/1490470967p5/45372.jpg')
        time.sleep(40)

    def test_ScrapeAuthorPage2(self):
        URL = 'https://www.goodreads.com/book/show/3735293-clean-code'
        try:
            retArr = scrapeAuthorPage(URL)
        except:
            retArr = None
        self.assertEqual(retArr, None)
        
    def test_handleCheckAuthor(self):
        author = {"name": 'bob',
            "author_url" : 'bob.com',
            "author_id" : '1234',
            "rating" : '4321',
            "rating_count" : '3333',
            "review_count" : '4444',
            "image_url" : 'bobimg.com',
            "related_authors" : '',
            "author_books" : ''}
        flag = checkIfAuthor(author)
        self.assertEqual(flag, True)
            
    def test_handleCheckAuthor2(self):
        book = {"book_url": 'book.com',
            "title" : 'book',
            "book_id" : '123',
            "ISBN" : '321',
            "author_url" : 'bob.com',
            "author" : 'bob',
            "rating" : '133',
            "rating_count" : '412',
            "review_count" : '135',
            "image_url" : 'bookimg.com',
            "similar_books" : ''}
        flag = checkIfAuthor(book)
        self.assertEqual(flag, False)
                
    def test_handleCheckBook(self):
        book = {"book_url": 'book.com',
            "title" : 'book',
            "book_id" : '123',
            "ISBN" : '321',
            "author_url" : 'bob.com',
            "author" : 'bob',
            "rating" : '133',
            "rating_count" : '412',
            "review_count" : '135',
            "image_url" : 'bookimg.com',
            "similar_books" : ''}
        flag = checkIfBook(book)
        self.assertEqual(flag, True)
        
    def test_handleCheckBook2(self):
        author = {"name": 'bob',
            "author_url" : 'bob.com',
            "author_id" : '1234',
            "rating" : '4321',
            "rating_count" : '3333',
            "review_count" : '4444',
            "image_url" : 'bobimg.com',
            "related_authors" : '',
            "author_books" : ''}
        flag = checkIfBook(author)
        self.assertEqual(flag, False)
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()