import pymongo
#===============================================================================
# This function handles when a book is being created or an already existing book is being updated in the MongoDB database.
#===============================================================================
def handleReadBooks(JSONFile):
    client = pymongo.MongoClient("mongodb+srv://JohnIm:4MY7jaApcsPmj4Kl@cluster0.0fsik.mongodb.net/Cluster0?retryWrites=true&w=majority")
    db = client.GoodReadData
    collection = db.Books
    collection.update(JSONFile, JSONFile, upsert = True)

#===============================================================================
# This function handles when an author is being created or an already existing book is being updated in the MongoDB database.
#===============================================================================
def handleReadAuthors(JSONFile):
    client = pymongo.MongoClient("mongodb+srv://JohnIm:4MY7jaApcsPmj4Kl@cluster0.0fsik.mongodb.net/Cluster0?retryWrites=true&w=majority")
    db = client.GoodReadData
    collection = db.Authors
    collection.update(JSONFile, JSONFile, upsert = True)
    
#===============================================================================
# This function handles the web scraped data of a book and transfers it into the MongoDB database.
#===============================================================================
def databaseBookHandler(retArr1):
    client = pymongo.MongoClient("mongodb+srv://JohnIm:4MY7jaApcsPmj4Kl@cluster0.0fsik.mongodb.net/Cluster0?retryWrites=true&w=majority")
    db = client.GoodReadData
    collection = db.Books   
    
    book = {"book_url": retArr1[0],
            "title" : retArr1[1],
            "book_id" : retArr1[2],
            "ISBN" : retArr1[3],
            "author_url" : retArr1[4],
            "author" : retArr1[5],
            "rating" : retArr1[6],
            "rating_count" : retArr1[7],
            "review_count" : retArr1[8],
            "image_url" : retArr1[9],
            "similar_books" : retArr1[10]}
  
    collection.update(book, book, upsert = True)
    
#===============================================================================
# # This function handles the web scraped data of an Author and transfers it into the MongoDB database.
#===============================================================================
def databaseAuthorHandler(retArr1):
    client = pymongo.MongoClient("mongodb+srv://JohnIm:4MY7jaApcsPmj4Kl@cluster0.0fsik.mongodb.net/Cluster0?retryWrites=true&w=majority")
    db = client.GoodReadData
    collection = db.Authors
    
    author= {"name": retArr1[0],
            "author_url" : retArr1[1],
            "author_id" : retArr1[2],
            "rating" : retArr1[3],
            "rating_count" : retArr1[4],
            "review_count" : retArr1[5],
            "image_url" : retArr1[6],
            "related_authors" : retArr1[7],
            "author_books" : retArr1[8],}

    
    collection.update(author, author, upsert = True)

    