"""
Tests
"""
import unittest
import time
from scraper import scrape_book_page, scrape_author_page, url_in_robots_file
from command import check_if_author, check_if_book

class Test(unittest.TestCase):
    """
    Test class for most functionality aside from database handling
    """
    def test_url_in_robots_file(self):
        """
        test
        """
        url = 'https://www.goodreads.com/book/show/52976360-coronavirus-and-christ'
        flag = url_in_robots_file(url)
        self.assertEqual(flag, True)
    def test_url_in_robots_file2(self):
        """
        test
        """
        url = 'https://www.goodreads.com/book/show/3735293-clean-code'
        flag = url_in_robots_file(url)
        self.assertEqual(flag, False)
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
        time.sleep(40)
    def test_scrape_book_page2(self):
        """
        test
        """
        url = 'https://www.goodreads.com/author/show/45372.Robert_C_Martin'
        try:
            ret_arr = scrape_book_page(url)
        except:
            ret_arr = None
        self.assertEqual(ret_arr, None)
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
        time.sleep(40)
    def test_scrape_author_page2(self):
        """
        test
        """
        url = 'https://www.goodreads.com/book/show/3735293-clean-code'
        try:
            ret_arr = scrape_author_page(url)
        except:
            ret_arr = None
        self.assertEqual(ret_arr, None)
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
if __name__ == "__main__":
    unittest.main()
    