"""
Implements the API handling and command-line interface of assignment-2.1 part3
"""
import datetime
import requests
import json
import pymongo
import argparse
from flask import Flask, request, jsonify
from database import get_key, database_book_handler, database_author_handler
from Parser import parseAfterColon, parseAfterLessThan
from Parser import parseAfterNOT, parseAfterGreaterThan
from Parser import parseAfterQuotes, dot, less_than, greater_than
from Parser import quote, colon, not_colon, parseBeforeORAfterColon
from Parser import not_quote, parseBeforeANDAfterColon, parseAfterAND
from Parser import or_colon, or_quotes, and_colon, and_quotes
from scraper import scrape_book_page, scrape_author_page


app = Flask(__name__)

def show_output(arr):
    """
    Helper function to format an output response of books or authors
    """
    output = []
    if arr[1] == 'book':
        for book in arr[0]:
            output.append({"book_url" : book['book_url'],
            'title' :  book['title'],
            'book_id' : book['book_id'],
            'ISBN' : book['ISBN'],
            'author_url' : book['author_url'],
            'author' : book['author'],
            'rating' : book['rating'],
            'rating_count' : book['rating_count'],
            'review_count' : book['review_count'],
            'image_url' : book['image_url'],
            'similar_books' : book['similar_books']})
        if len(output) == 0:
            return None
        return jsonify(output)
    if arr[1] == 'author':
        for author in arr[0]:
            output.append({"name": author['name'],
            "author_url" : author['author_url'],
            "author_id" : author['author_id'],
            "rating" : author['rating'],
            "rating_count" : author['rating_count'],
            "review_count" : author['review_count'],
            "image_url" : author['image_url'],
            "related_authors" : author['related_authors'],
            "author_books" : author['author_books']})
        if len(output) == 0:
            return None
        return jsonify(output)
@app.route('/search', methods=['GET'])
def get_query():
    """
    Function to handle an API GET request for a query string.
    """
    query_string = request.args.get("q")
    output = []
    if not query_string :
        output = {'time' : datetime.datetime.now(), 'status' : 400,
                  'message' : 'Query String did not result in a valid search'}
        return jsonify(output)
    elif parseAfterColon(query_string) is None:
        arr = dot(query_string)
        if show_output(arr) is None:
            output = {'time' : datetime.datetime.now(), 'status' : 400,
                      'message' : 'Query String did not result in a valid search'}
            return jsonify(output)
        return show_output(arr)
    elif parseAfterColon(query_string) and parseAfterLessThan(query_string):
        arr = less_than(query_string)
        if show_output(arr) is None:
            output = {'time' : datetime.datetime.now(), 'status' : 400,
                      'message' : 'Query String did not result in a valid search'}
            return jsonify(output)
        return show_output(arr)
    elif parseAfterColon(query_string) and parseAfterGreaterThan(query_string):
        arr = greater_than(query_string)
        if show_output(arr) is None:
            output = {'time' : datetime.datetime.now(), 'status' : 400,
                      'message' : 'Query String did not result in a valid search'}
            return jsonify(output)
        return show_output(arr)
    elif (parseAfterColon(query_string) and parseBeforeANDAfterColon(query_string)
          and parseAfterQuotes(query_string) is None):
        arr = and_colon(query_string)
        if show_output(arr) is None:
            output = {'time' : datetime.datetime.now(), 'status' : 400,
                      'message' : 'Query String did not result in a valid search'}
            return jsonify(output)
        return show_output(arr)
    elif (parseAfterQuotes(query_string) and parseBeforeANDAfterColon(query_string)
          and parseAfterQuotes(query_string)):
        arr = and_quotes(query_string)
        if show_output(arr) is None:
            output = {'time' : datetime.datetime.now(), 'status' : 400,
                      'message' : 'Query String did not result in a valid search'}
            return jsonify(output)
        return show_output(arr)
    elif (parseAfterColon(query_string) and parseAfterQuotes(query_string) is None
           and parseBeforeORAfterColon(query_string)):
        arr = or_colon(query_string)
        if show_output(arr) is None:
            output = {'time' : datetime.datetime.now(), 'status' : 400,
                      'message' : 'Query String did not result in a valid search'}
            return jsonify(output)
        return show_output(arr)
    elif (parseAfterColon(query_string) and parseAfterQuotes(query_string)
          and parseBeforeORAfterColon(query_string)):
        arr = or_quotes(query_string)
        if show_output(arr) is None:
            output = {'time' : datetime.datetime.now(), 'status' : 400,
                      'message' : 'Query String did not result in a valid search'}
            return jsonify(output)
        return show_output(arr)
    elif (parseAfterColon(query_string) and parseAfterNOT(query_string)
          and parseAfterQuotes(query_string)):
        arr = not_quote(query_string)
        if show_output(arr) is None:
            output = {'time' : datetime.datetime.now(), 'status' : 400,
                      'message' : 'Query String did not result in a valid search'}
            return jsonify(output)
        return show_output(arr)
    elif parseAfterColon(query_string) and parseAfterNOT(query_string):
        arr = not_colon(query_string)
        if show_output(arr) is None:
            output = {'time' : datetime.datetime.now(), 'status' : 400,
                      'message' : 'Query String did not result in a valid search'}
            return jsonify(output)
        return show_output(arr)
    elif parseAfterColon(query_string) and parseAfterQuotes(query_string):
        arr = quote(query_string)
        if show_output(arr) is None:
            output = {'time' : datetime.datetime.now(), 'status' : 400,
                      'message' : 'Query String did not result in a valid search'}
            return jsonify(output)
        return show_output(arr)
    elif (parseAfterColon(query_string) and parseAfterQuotes(query_string) is None
          and parseAfterAND(query_string) is None and parseAfterLessThan(query_string) is None
            and parseAfterLessThan(query_string) is None):
        arr = colon(query_string)
        if show_output(arr) is None:
            output = {'time' : datetime.datetime.now(), 'status' : 400,
                      'message' : 'Query String did not result in a valid search'}
            return jsonify(output)
        return show_output(arr)
    else:
        output = {'time' : datetime.datetime.now(), 'status' : 400,
                  'message' : 'Query String did not result in a valid search'}
        return jsonify(output)
@app.route('/author', methods=['GET'])
def get_author_by_id():
    """
    Helper function for an API GET request via author ID lookup
    """
    author_id = request.args.get("id")
    client = pymongo.MongoClient(get_key())
    data_base = client['GoodReadData']
    authors = data_base["Authors"]
    output = []
    author = authors.find_one({'author_id' : author_id})
    if author:
        output.append({"name": author['name'],
                "author_url" : author['author_url'],
                "author_id" : author['author_id'],
                "rating" : author['rating'],
                "rating_count" : author['rating_count'],
                "review_count" : author['review_count'],
                "image_url" : author['image_url'],
                "related_authors" : author['related_authors'],
                "author_books" : author['author_books']})
        return jsonify(output)
    output = {'time' : datetime.datetime.now(), 'status' : 400,
                  'message' : 'No such author ID exists'}
    return jsonify(output)
@app.route('/book', methods=['GET'])
def get_book_by_id():
    """
    Helper function for an API GET request via book ID lookup
    """
    book_id = request.args.get("id")
    client = pymongo.MongoClient(get_key())
    data_base = client['GoodReadData']
    books = data_base["Books"]
    output = []
    book = books.find_one({'book_id' : book_id})
    if book:
        output.append({"book_url" : book['book_url'],
        'title' :  book['title'],
        'book_id' : book['book_id'],
        'ISBN' : book['ISBN'],
        'author_url' : book['author_url'],
        'author' : book['author'],
        'rating' : book['rating'],
        'rating_count' : book['rating_count'],
        'review_count' : book['review_count'],
        'image_url' : book['image_url'],
        'similar_books' : book['similar_books']})
        return jsonify(output)
    output = {'time' : datetime.datetime.now(), 'status' : 400,
                  'message' : 'No such book ID exists'}
    return jsonify(output)
@app.route('/book', methods=['PUT'])
def put_book_id():
    """
    Helper function for an API PUT request via author ID lookup
    """
    book_id = request.args.get("id")
    client = pymongo.MongoClient(get_key())
    data_base = client['GoodReadData']
    books = data_base["Books"]
    book = books.find_one({'book_id' : book_id})
    req = request.get_json()
    if book:
        books.update({'book_id' : book_id}, {'$set' : req})
        return 'updated ' + book_id
    output = {'time' : datetime.datetime.now(), 'status' : 400,
                  'message' : 'No such book ID exists'}
    return jsonify(output)
@app.route('/author', methods=['PUT'])
def put_author_id():
    """
    Helper function for an API PUT request via author ID lookup
    """
    author_id = request.args.get("id")
    client = pymongo.MongoClient(get_key())
    data_base = client['GoodReadData']
    authors = data_base["Authors"]
    author = authors.find_one({'author_id' : author_id})
    req = request.get_json()
    if author:
        authors.update({'author_id' : author_id}, {'$set' : req})
        return 'updated ' + author_id
    output = {'time' : datetime.datetime.now(), 'status' : 400,
                  'message' : 'No such book ID exists'}
    return jsonify(output)
@app.route('/book', methods=['POST'])
def add_book():
    """
    Helper function for an API POST request to add a single book
    """
    output = []
    req = request.get_json()
    if not req:
        output = {'time' : datetime.datetime.now(), 'status' : 400,
                  'message' : 'No body was provided'}
        return jsonify(output)
    temp = list(req.values())
    database_book_handler(temp)
    output.append({'book_url': temp[0],
                'title' : temp[1],
                'book_id' : temp[2],
                'ISBN' : temp[3],
                'author_url' : temp[4],
                'author' : temp[5],
                'rating' : temp[6],
                'rating_count' : temp[7],
                'review_count' : temp[8],
                'image_url' : temp[9],
                'similar_books' : temp[10]})
    return jsonify(output)
@app.route('/books', methods=['POST'])
def add_books():
    """
    Helper function for an API POST request to multiple books
    """
    output = []
    req = request.get_json()
    if not req:
        output = {'time' : datetime.datetime.now(), 'status' : 400,
                  'message' : 'No body was provided'}
        return jsonify(output)
    for res in req:
        temp = list(res.values())
        database_book_handler(temp)
        output.append({'book_url': temp[0],
                    'title' : temp[1],
                    'book_id' : temp[2],
                    'ISBN' : temp[3],
                    'author_url' : temp[4],
                    'author' : temp[5],
                    'rating' : temp[6],
                    'rating_count' : temp[7],
                    'review_count' : temp[8],
                    'image_url' : temp[9],
                    'similar_books' : temp[10]})
    return jsonify(output)
@app.route('/author', methods=['POST'])
def add_author():
    """
    Helper function for an API POST request to add a single author
    """
    output = []
    req = request.get_json()
    if not req:
        output = {'time' : datetime.datetime.now(), 'status' : 400,
                  'message' : 'No body was provided'}
        return jsonify(output)
    name = request.json['name']
    author_url = request.json['author_url']
    author_id = request.json['author_id']
    rating = request.json['rating']
    rating_count = request.json['rating_count']
    review_count = request.json['review_count']
    image_url = request.json['image_url']
    related_authors = request.json['related_authors']
    author_books = request.json['author_books']

    ret_arr1 = [name, author_url, author_id, rating, rating_count,
                review_count, image_url, related_authors, author_books]
    database_author_handler(ret_arr1)
    output = {"name": ret_arr1[0],
                "author_url" : ret_arr1[1],
                "author_id" : ret_arr1[2],
                "rating" : ret_arr1[3],
                "rating_count" : ret_arr1[4],
                "review_count" : ret_arr1[5],
                "image_url" : ret_arr1[6],
                "related_authors" : ret_arr1[7],
                "author_books" : ret_arr1[8]}
    return jsonify(output)
@app.route('/authors', methods=['POST'])
def add_authors():
    """
    Helper function for an API POST request to multiple authors
    """
    output = []
    req = request.get_json()
    if not req:
        output = {'time' : datetime.datetime.now(), 'status' : 400,
                  'message' : 'No body was provided'}
        return jsonify(output)
    for res in req:
        temp = list(res.values())
        database_author_handler(temp)
        output.append({"name": temp[0],
                "author_url" : temp[1],
                "author_id" : temp[2],
                "rating" : temp[3],
                "rating_count" : temp[4],
                "review_count" : temp[5],
                "image_url" : temp[6],
                "related_authors" : temp[7],
                "author_books" : temp[8]})
    return jsonify(output)
@app.route('/scrape', methods=['POST'])
def add_new_scrapes():
    """
    Helper function for an API POST request to handle scraping and database
    """
    url = request.args.get("url")
    if 'book' in url and scrape_book_page(url) is not None:
        arr1 = scrape_book_page(url)
        database_book_handler(arr1)
        return 'successfully scraped book'
    if 'author' in url and scrape_author_page(url) is not None:
        arr1 = scrape_author_page(url)
        database_author_handler(arr1)
        return 'successfully scraped author'
    output = {'time' : datetime.datetime.now(), 'status' : 400,
                  'message' : 'No scrape was performed due to invalid input'}
    return jsonify(output)
@app.route('/book', methods=['DELETE'])
def delete_book():
    """
    Helper function for an API DELETE request to delete a single book
    """
    book_id = request.args.get("id")
    client = pymongo.MongoClient(get_key())
    data_base = client['GoodReadData']
    books = data_base["Books"]
    book  = books.find_one({'book_id' : book_id})
    if book:
        query = {'book_id' : book_id}
        books.delete_one(query)
        return 'deleted book with id ' + book_id
    output = {'time' : datetime.datetime.now(), 'status' : 400,
                  'message' : 'No scrape was performed due to invalid input'}
    return jsonify(output)
@app.route('/author', methods=['DELETE'])
def delete_author():
    """
    Helper function for an API DELETE request to delete a single author
    """
    author_id = request.args.get("id")
    client = pymongo.MongoClient(get_key())
    data_base = client['GoodReadData']
    authors = data_base["Authors"]
    output = []
    author  = authors.find_one({'author_id' : author_id})
    if author:
        query = {'author_id' : author_id}
        authors.delete_one(query)
        return 'deleted author with id ' + author_id
    output = {'time' : datetime.datetime.now(), 'status' : 400,
                  'message' : 'No scrape was performed due to invalid input'}
    return jsonify(output)
def main():
    """
    Main function to handle command-line interface
    """
    parser = argparse.ArgumentParser(description = 'Parse user Input')
    parser.add_argument('command', help = "Enter a command : GET, PUT, POST, DELETE")
    parser.add_argument('-id', '--field_content', help = "example input is : book.book_id:1")
    parser.add_argument('-up', '--File', required = False,
                        help = "Supply a valid JSON File to update or insert the database entry to")
    args = parser.parse_args()
    if args.command == 'GET':
        if 'book' in args.field_content:
            result = parseAfterColon(args.field_content)
            response = requests.get('http://127.0.0.1:5000/book', params={'id': result})
            print(response.text)
        if 'author' in args.field_content:
            result = parseAfterColon(args.field_content)
            response = requests.get('http://127.0.0.1:5000/author', params={'id': result})
            print(response.text)
    if args.command == 'PUT':
        if 'book' in args.field_content and args.File is not None:
            result = parseAfterColon(args.field_content)
            file = open(args.File, 'r')
            data = json.load(file)
            response = requests.put('http://127.0.0.1:5000/book',
                                    params={'id': result}, json = data)
            print(response.text)
        if 'author' in args.field_content and args.File is not None:
            result = parseAfterColon(args.field_content)
            file = open(args.File, 'r')
            data = json.load(file)
            response = requests.put('http://127.0.0.1:5000/author',
                                    params={'id': result}, json = data)
            print(response.text)
    if args.command == 'POST':
        if 'book' in args.field_content and args.File is not None:
            result = parseAfterColon(args.field_content)
            file = open(args.File, 'r')
            data = json.load(file)
            response = requests.post('http://127.0.0.1:5000/book', json = data)
            print(response.text)
        if 'author' in args.field_content and args.File is not None:
            result = parseAfterColon(args.field_content)
            file = open(args.File, 'r')
            data = json.load(file)
            response = requests.post('http://127.0.0.1:5000/author', json = data)
            print(response.text)
    if args.command == 'DELETE':
        if 'book' in args.field_content:
            result = parseAfterColon(args.field_content)
            response = requests.delete('http://127.0.0.1:5000/book', params={'id': result})
            print(response.text)
        if 'author' in args.field_content:
            result = parseAfterColon(args.field_content)
            response = requests.delete('http://127.0.0.1:5000/author', params={'id': result})
            print(response.text)
if __name__ == "__main__":
    main()
        