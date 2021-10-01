"""
Implements the transferring of web scraped data to a MongoDB database
"""
import pymongo
import os
from dotenv import load_dotenv

def get_key():
    """
    This function gets the unique key to access my MongoDB database collection
    """
    load_dotenv("./key.env")
    return os.getenv("SECRET_KEY")
def handle_read_books(json_file):
    """
    This function handles when a book is being created or an already existing book is being updated in the MongoDB database.
    """
    client = pymongo.MongoClient(get_key())
    database = client.GoodReadData
    collection = database.Books
    collection.update(json_file, json_file, upsert = True)
def handle_read_authors(json_file):
    """
    This function handles when an author is being created or an already existing book is being updated in the MongoDB database.
    """
    client = pymongo.MongoClient(get_key())
    database = client.GoodReadData
    collection = database.Authors
    collection.update(json_file, json_file, upsert = True)
def database_book_handler(ret_arr1):
    """
    This function handles the web scraped data of a book and transfers it into the MongoDB database.
    """
    if ret_arr1 is not None:
        client = pymongo.MongoClient(get_key())
        database = client.GoodReadData
        collection = database.Books
        book = {"book_url": ret_arr1[0],
                "title" : ret_arr1[1],
                "book_id" : ret_arr1[2],
                "ISBN" : ret_arr1[3],
                "author_url" : ret_arr1[4],
                "author" : ret_arr1[5],
                "rating" : ret_arr1[6],
                "rating_count" : ret_arr1[7],
                "review_count" : ret_arr1[8],
                "image_url" : ret_arr1[9],
                "similar_books" : ret_arr1[10]}
        collection.update(book, book, upsert = True)
def database_author_handler(ret_arr1):
    """
    This function handles the web scraped data of an Author and transfers it into the MongoDB database.
    """
    if ret_arr1 is not None:
        client = pymongo.MongoClient(get_key())
        database = client.GoodReadData
        collection = database.Authors
        author = {"name": ret_arr1[0],
                "author_url" : ret_arr1[1],
                "author_id" : ret_arr1[2],
                "rating" : ret_arr1[3],
                "rating_count" : ret_arr1[4],
                "review_count" : ret_arr1[5],
                "image_url" : ret_arr1[6],
                "related_authors" : ret_arr1[7],
                "author_books" : ret_arr1[8]}
        collection.update(author, author, upsert = True)
    
if __name__ == "__main__":
    print(get_key())
    