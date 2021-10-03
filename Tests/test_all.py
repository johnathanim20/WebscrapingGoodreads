"""
Tests
"""
import unittest
import sys
sys.path.insert(1, 'C:\\Users\\johna\\fa21-cs242-assignment-2\\src')
import pytest
import requests
import json
from scraper import scrape_book_page, scrape_author_page, url_in_robots_file
from command import check_if_author, check_if_book
from Parser import parseAfterDotBeforeColon, parseBeforeDot, parseAfterDot, parseAfterColon, parseBeforeANDAfterColon, parseAfterQuotes, parseAfterAND

class Test(unittest.TestCase):
    """
    Test class for most functionality aside from database handling
    """
    def test_add_book(self):
        test_file = {'book_url' : 'https://www.goodreads.com/book/show/44936.Refactoring',
                'title' : 'Refactoring: Improving the Design of Existing Code',
                'book_id': '44936',
                'ISBN' : '9780201485677',
                'author_url' : 'https://www.goodreads.com/author/show/25215.Martin_Fowler',
                'author' : 'Martin Fowler',
                'rating' : '4.25',
                'rating_count' : '7420',
                'review_count' : '309',
                'image_url' : 'https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/...',
                'similar_books' : 'https://www.goodreads.com/book/show/85009.Design_Patterns%22%7D'}
        response = requests.post('http://127.0.0.1:5000/book', json=test_file)
        self.assertEqual(response.status_code, 200)
        
    def test_add_author(self):
        test_file = {"name" : "John",
                    "author_url": "https://john.com",
                    "author_id" : "2",
                    "rating" : "1",
                    "rating_count" : "45",
                    "review_count" : "33",
                    "image_url" : "https://john.com",
                    "related_authors" : "pk",
                    "author_books" : "ex"}
        response = requests.post('http://127.0.0.1:5000/author', json=test_file)
        self.assertEqual(response.status_code, 200)
    
    def test_get_book(self):
        #=======================================================================
        # test_file = {'book_url' : 'https://www.goodreads.com/book/show/44936.Refactoring',
        #         'title' : 'Refactoring: Improving the Design of Existing Code',
        #         'book_id': '44936',
        #         'ISBN' : '9780201485677',
        #         'author_url' : 'https://www.goodreads.com/author/show/25215.Martin_Fowler',
        #         'author' : 'Martin Fowler',
        #         'rating' : '4.25',
        #         'rating_count' : '7420',
        #         'review_count' : '309',
        #         'image_url' : 'https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/...',
        #         'similar_books' : 'https://www.goodreads.com/book/show/85009.Design_Patterns%22%7D'}
        #=======================================================================
        response = requests.get('http://127.0.0.1:5000/book', params={'id':"44936"})
        self.assertEqual(response.status_code, 200)
    def test_get_author(self):
        #=======================================================================
        # test_file = {"name" : "John",
        #            "author_url": "https://john.com",
        #            "author_id" : "2",
        #            "rating" : "1",
        #            "rating_count" : "45",
        #            "review_count" : "33",
        #            "image_url" : "https://john.com",
        #            "related_authors" : "pk",
        #            "author_books" : "ex"}
        #=======================================================================
        response = requests.get('http://127.0.0.1:5000/author', params={'id':"2"})
        self.assertEqual(response.status_code, 200)
    def test_update_author(self):
        test_file = {"name" : "John2",
                    "author_url": "https://john2.com",
                    "author_id" : "2",
                    "rating" : "2",
                    "rating_count" : "46",
                    "review_count" : "34",
                    "image_url" : "https://john2.com",
                    "related_authors" : "pk2",
                    "author_books" : "ex2"}
        response = requests.put('http://127.0.0.1:5000/author', params={'id' : 2},  json=test_file)
        print(response.text)
        self.assertEqual(response.status_code, 200)
        
    def test_scrape_book_page(self):
        """
        test
        """
        url = 'https://www.goodreads.com/book/show/3735293-clean-code'
        ret_arr = scrape_book_page(url)
        self.assertEqual(ret_arr[0], 'https://www.goodreads.com/book/show/3735293-clean-code')
        self.assertEqual(ret_arr[1], 'Clean Code: A Handbook of Agile Software Craftsmanship')
        self.assertEqual(ret_arr[2], '3735293')
        self.assertEqual(ret_arr[3], '9780132350884')
        self.assertEqual(ret_arr[4], 'https://www.goodreads.com/author/show/45372.Robert_C_Martin')
        self.assertEqual(ret_arr[5], 'Robert C. Martin')
        self.assertEqual(ret_arr[9], 'https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1436202607l/3735293._SX318_.jpg')
        #time.sleep(40)
    def test_scrape_book_page2(self):
        """
        test
        """
        url = 'https://www.goodreads.com/author/show/45372.Robert_C_Martin'
        try:
            ret_arr = scrape_book_page(url)
        except:
            ret_arr = None
        self.assertEqual(ret_arr[1], '')
    def test_scrape_author_page(self):
        """
        test
        """
        url = 'https://www.goodreads.com/author/show/45372.Robert_C_Martin'
        ret_arr = scrape_author_page(url)
        self.assertEqual(ret_arr[0], 'Robert C. Martin')
        self.assertEqual(ret_arr[1], 'https://www.goodreads.com/author/show/45372.Robert_C_Martin')
        self.assertEqual(ret_arr[2], '45372')
        #self.assertEqual(retArr[3], '4.34')
        #self.assertEqual(retArr[4], '31522')
        #self.assertEqual(retArr[5], '2093')
        self.assertEqual(ret_arr[6], 'https://images.gr-assets.com/authors/1490470967p5/45372.jpg')
        #time.sleep(40)
    def test_scrape_author_page2(self):
        """
        test
        """
        url = 'https://www.goodreads.com/book/show/3735293-clean-code'
        try:
            ret_arr = scrape_author_page(url)
        except:
            ret_arr = None
        self.assertEqual(ret_arr[8], '')
    def test_handle_check_author(self):
        """
        test
        """
        author = {"name": 'bob',
            "author_url" : 'bob.com',
            "author_id" : '1234',
            "rating" : '4321',
            "rating_count" : '3333',
            "review_count" : '4444',
            "image_url" : 'bobimg.com',
            "related_authors" : '',
            "author_books" : ''}
        flag = check_if_author(author)
        self.assertEqual(flag, True)
    def test_handle_check_author2(self):
        """
        test
        """
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
        flag = check_if_author(book)
        self.assertEqual(flag, False)
    def test_handle_check_book(self):
        """
        test
        """
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
        flag = check_if_book(book)
        self.assertEqual(flag, True)
    def test_handle_check_book2(self):
        """
        test
        """
        author = {"name": 'bob',
            "author_url" : 'bob.com',
            "author_id" : '1234',
            "rating" : '4321',
            "rating_count" : '3333',
            "review_count" : '4444',
            "image_url" : 'bobimg.com',
            "related_authors" : '',
            "author_books" : ''}
        flag = check_if_book(author)
        self.assertEqual(flag, False)
        
    def test_parse_before_dot(self):
        string = 'book.book_id'
        result = parseBeforeDot(string)
        self.assertEqual('book', result)
    def test_parse_after_dot(self):
        string = 'book.book_id'   
        result = parseAfterDot(string)
        self.assertEqual('book_id', result)
    def test_parse_after_colon(self):
        string = 'book.book_id:123'
        result =  parseAfterColon(string)
        self.assertEqual('123', result)   
    def test_parse_after_quotes(self):
        string = "book.book_id:'123'"
        result = parseAfterQuotes(string)
        self.assertEqual('123', result)
    def test_after_and(self):
        string = "book.book_id:123AND321"
        result = parseAfterAND(string)
        self.assertEqual('321', result)
    def test_before_and_after_colon(self):
        string = "book.book_id:123AND321"
        result = parseBeforeANDAfterColon(string)
        self.assertEqual('123', result)
    def test_after_dot_before_colon(self):
        string = "book.book_id:123AND321"
        result = parseAfterDotBeforeColon(string)
        self.assertEqual('book_id', result)
        
    
if __name__ == "__main__":
    unittest.main()
    