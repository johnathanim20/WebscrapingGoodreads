from flask import Flask, request, jsonify
import datetime
from database import get_key, database_book_handler
import pymongo
import argparse
from Parser import parseAfterColon, parseBeforeDot, parseAfterDotBeforeColon, handleColonCommand,\
    parseAfterQuotes



app = Flask(__name__)

def handleColonQuery(query_string):
    output = []
    string1 = parseAfterColon(query_string)
    string2 = parseBeforeDot(query_string)
    string3 = parseAfterDotBeforeColon(query_string)
    arr = handleColonCommand(string3, string2, string1)
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
        return jsonify(output)
    else:
        output = {'time' : datetime.datetime.now(), 'status' : 400 , 'message' : 'Query String did not result in a valid search'}
        return jsonify(output)

@app.route('/search/<query_string>', methods=['GET'])
def get_query(query_string):
#handles a '.' operation followed by a colon operation
    if (parseAfterColon(query_string) is None):
        handleColonQuery(query_string)

@app.route('/book/<author_id>', methods=['GET'])
def get_author_by_id(author_id):
    client = pymongo.MongoClient(get_key())
    data_base = client['GoodReadData']
    authors = data_base["Authors"]
    output = []
    string = parseAfterColon(author_id)
    author = authors.find_one({'author_id' : string})
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
    else:
        output = {'time' : datetime.datetime.now(), 'status' : 400 , 'message' : 'No such author ID exists'}
        return jsonify(output)
    
@app.route('/book/<book_id>', methods=['GET'])
def get_book_by_id(book_id):
    client = pymongo.MongoClient(get_key())
    data_base = client['GoodReadData']
    books = data_base["Books"]
    output = []
    string = parseAfterColon(book_id)
    book = books.find_one({'book_id' : string})
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
    else:
        output = {'time' : datetime.datetime.now(), 'status' : 400 , 'message' : 'No such book ID exists'}
        return jsonify(output)

@app.route('/book/<book_id>', methods=['PUT'])
def put_book_id(book_id):
    return
@app.route('/book', methods=['POST'])
def add_book():
    book_url = request.json['book_url']
    title = request.json['title']
    book_id = request.json['book_id']
    isbn = request.json['ISBN']
    author_url = request.json['author_url']
    author = request.json['author']
    rating = request.json['rating']
    rating_count = request.json['rating_count']
    review_count = request.json['review_count']
    image_url = request.json['image_url']
    similar_books = request.json['similar_books']

    ret_arr1 = [book_url, title, book_id, isbn, author_url, author, rating, rating_count, review_count, image_url, similar_books]
    database_book_handler(ret_arr1)
    output = {'book_url': ret_arr1[0],
                'title' : ret_arr1[1],
                'book_id' : ret_arr1[2],
                'ISBN' : ret_arr1[3],
                'author_url' : ret_arr1[4],
                'author' : ret_arr1[5],
                'rating' : ret_arr1[6],
                'rating_count' : ret_arr1[7],
                'review_coun' : ret_arr1[8],
                'image_url' : ret_arr1[9],
                'similar_books' : ret_arr1[10]}
    return jsonify(output)
