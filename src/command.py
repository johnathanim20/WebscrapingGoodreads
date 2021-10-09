"""
Implements the command line interface so that the user can choose inputs for the program.
"""
import argparse
import time
import json
import pymongo
from scraper import scrape_author_page, scrape_book_page, url_in_robots_file
from database import database_author_handler, handle_read_authors, handle_read_books, database_book_handler, get_key
from pylint.checkers import similar


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
    
        
        similar_book_urls = []
        similar_author_urls = []
        count = 0
        num_books = 0
        num_authors = 0
        url = args.Book_URL
        while True:
            similar_book_urls.append(url)
            print('Begin scraping a page')
            ret_arr = scrape_book_page(url)
            #===================================================================
            # if ret_arr is None:
            #     continue
            #===================================================================
            database_book_handler(ret_arr)
            [similar_book_urls.append(x) for x in ret_arr[10] if x not in similar_book_urls]
            num_books += 1
            time.sleep(15)
            print('Ended this scrape')
            url = similar_book_urls[count]
            count += 1
            if (num_books == args.Number_Of_Books):
                break
        url = ret_arr[4]
        count = 0
        while True:
            similar_author_urls.append(url)
            print('Begin scraping a page')
            ret_arr2 = scrape_author_page(url)
            #===================================================================
            # if ret_arr2 is None:
            #     continue
            #===================================================================
            database_author_handler(ret_arr2)
            [similar_author_urls.append(x) for x in ret_arr[7] if x not in similar_author_urls]
            num_authors += 1
            time.sleep(15)
            print('Ended this scrape') 
            url = similar_author_urls[count]
            count += 1
            if (num_authors == args.Number_Of_Authors):
                break
            
        read_json(args)
        write_json(args)
    else:
        print('Invalid book URL. Must be a valid book URL from Goodreads.com')
