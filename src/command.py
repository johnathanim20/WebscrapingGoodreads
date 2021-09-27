"""
Implements the command line interface so that the user can choose inputs for the program.
"""
import argparse
import time
import json
import pymongo
from scraper import scrape_author_page, scrape_book_page, url_in_robots_file
from database import database_author_handler, handle_read_authors, handle_read_books, database_book_handler, get_key


def check_if_book(document):
    """
    Function to see if a Document is a Book
    """
    return bool('book_url' in document.keys())
def check_if_author(document):
    """
    Function to see if a Document is an Author
    """
    return bool('author_id' in document.keys())
def read_json(arg):
    """
    Function to handle reading a JSON File and updating
    or creating new entries in the MongoDB database
    """
    data = None
    if arg.JSON_File_In is not None:
        file = open(arg.JSON_File_In, 'r')
        data = json.load(file)
        if isinstance(data, dict):
            if check_if_author(data):
                handle_read_authors(data)
            else:
                handle_read_books(data)
        else:
            for entry in data:
                if check_if_author(entry):
                    handle_read_authors(entry)
                else:
                    handle_read_books(entry)
        file.close()
def write_json(arg):
    """
    Function to handle writing to a JSON File using JSON Data
    being exported from the MongoDB database.
    """
    if (args.JSON_File_Out is not None and args.input is not None) :
        client = pymongo.MongoClient(get_key())
        data_base = client['GoodReadData']
        books = data_base["Books"]
        authors = data_base["Authors"]
        for book in books.find():
            if arg.input == str(book['book_url']):
                with open(arg.JSON_File_Out, "w") as outfile:
                    json.dump(str(book), outfile, indent = 4)
                    break
        for author in authors.find():
            if arg.input == str(author['author_url']):
                with open(arg.JSON_File_Out, "w") as outfile:
                    json.dump(str(author), outfile, indent = 4)
                    break
def run_book_handler(url, arg):
    """
    This function handles scraping, transferring data to MongoDB's
    database for the amount of books that the user specifies.
    """
    save_book_urls = []
    for index in range(arg.Number_Of_Books):
        save_book_urls.append(url)
        print('Begin scraping a page')
        ret_arr = scrape_book_page(URL)
        database_book_handler(ret_arr)
        time.sleep(40)
        url = ret_arr[10][index]
        for second in range(index):
            if url == save_book_urls[second]:
                url = ret_arr[10][second+1]
        increment = 0
        while True:
            if not url_in_robots_file(url):
                break
            else:
                increment+=1
                url = ret_arr[10][increment]
        print('Ended this scrape')
    return ret_arr[4]
def run_author_handler(url, arg):
    """
    This function handles scraping, transferring data to MongoDB's
    database for the amount of Authors that the user specifies.
    """
    save_author_urls = []
    for index in range(arg.Number_Of_Authors):
        save_author_urls.append(url)
        print('Begin scraping a page')
        ret_arr2 = scrape_author_page(url)
        database_author_handler(ret_arr2)
        time.sleep(40)
        url = ret_arr2[7][index]
        for increment in range(index+1):
            if url == save_author_urls[increment]:
                url = ret_arr2[7][increment+1]
        print('Ended this scrape')
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = 'Parse a Book')
    parser.add_argument('Book_URL', type=str, help = "GoodReads Book URL")
    parser.add_argument('Number_Of_Books', type=int,
                        help = "enter a number of books to scrape (between 1 and 200)")
    parser.add_argument('Number_Of_Authors', type=int,
                        help = "enter a number of Authors to scrape (between 1 and 50)")
    parser.add_argument('-in' ,'--JSON_File_In', required = False,
                        help = "enter a valid JSON File to read from")
    parser.add_argument('-existing' ,'--input', required = False,
                        help = "enter a valid Book URL or Author URL to Export")
    parser.add_argument('-out' ,'--JSON_File_Out', required = False,
                        help = "enter a JSON File to write to")
    args = parser.parse_args()
    if url_in_robots_file(args.Book_URL):
        print("The given url is contained within the robots.txt file and should not be used")
    if 'book' in args.Book_URL:
        if args.Number_Of_Books > 200 and args.Number_Of_Authors > 50:
            print("Scraping more than 200 Books and 50 Authors can damage the scraped website")
        URL = args.Book_URL
        authorURL = run_book_handler(URL, args)
        run_author_handler(authorURL, args)
        read_json(args)
        write_json(args)
    else:
        print('Invalid book URL. Must be a valid book URL from Goodreads.com')
