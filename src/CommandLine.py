import argparse
from Scraper import scrapeAuthorPage
from Scraper import scrapeBookPage
from Database import databaseAuthorHandler, handleReadAuthors, handleReadBooks
from Database import databaseBookHandler
from Scraper import urlInRobotsFile
import time
import json
import pymongo


#===============================================================================
# Function to see if a Document is a Book
#===============================================================================
def checkIfBook(Document):
    if 'book_url' in Document.keys():
        return True
    else:
        return False
    
#===============================================================================
# Function to see if a Document is an Author
#===============================================================================
def checkIfAuthor(Document):
    if 'author_id' in Document.keys():
        return True
    else:
        return False


#===============================================================================
# Function to handle reading a JSON File and updating or creating new entries in the MongoDB Database
#===============================================================================
def readJson(args):
    data = None
    if (args.JSON_File_In != None):
        f = open(args.JSON_File_In, 'r')
        data = json.load(f)
        if (type(data) is dict):
            if (checkIfAuthor(data)):
                handleReadAuthors(data)
            else:
                handleReadBooks(data)
        else: 
            for x in data:
                if (checkIfAuthor(x)):
                    handleReadAuthors(x)
                else :
                    handleReadBooks(x)
        f.close() 
        
#===============================================================================
# Function to handle writing to a JSON File using JSON Data being exported from the MongoDB Database.        
#===============================================================================
def writeJson(args):        
    #data = None
    if (args.JSON_File_Out != None and args.input != None) :
        client = pymongo.MongoClient("mongodb+srv://JohnIm:4MY7jaApcsPmj4Kl@cluster0.0fsik.mongodb.net/Cluster0?retryWrites=true&w=majority")
        db = client['GoodReadData']
        books = db["Books"]
        authors = db["Authors"]
        
        for x in books.find():
            if (args.input == str(x['book_url'])):
                with open(args.JSON_File_Out, "w") as outfile:
                    (json.dump(str(x), outfile, indent = 4))
                    break
        for x in authors.find():
            if (args.input == str(x['author_url'])):
                with open(args.JSON_File_Out, "w") as outfile:
                    (json.dump(str(x), outfile, indent = 4))
                    break
#===============================================================================
# This function handles scraping, transferring data to MongoDB's database for the amount of books that the user specifies.
#===============================================================================
def runBookHandler(URL, args):
    saveBookUrls = []
    for x in range(args.Number_Of_Books):
        saveBookUrls.append(URL)
        print('Begin scraping a page')
        retArr = scrapeBookPage(URL)
        databaseBookHandler(retArr)
        time.sleep(40)
        URL = retArr[10][x]
        for z in range(x):
            if (URL == saveBookUrls[z]):
                URL = retArr[10][z+1]
        j = 0
        while True:
            if (not urlInRobotsFile(URL)):
                break
            else:
                URL = retArr[10][++j]
        print('Ended this scrape')
    return retArr[4]    

#===============================================================================
# This function handles scraping, transferring data to MongoDB's database for the amount of Authors that the user specifies.
#===============================================================================
def runAuthorHandler(URL, args):
    saveAuthorUrls = []
    for x in range(args.Number_Of_Authors):
        saveAuthorUrls.append(URL)
        print('Begin scraping a page')
        retArr2 = scrapeAuthorPage(URL)
        databaseAuthorHandler(retArr2)
        time.sleep(40) 
        URL = retArr2[7][x]
        for z in range(x+1):
            if (URL == saveAuthorUrls[z]):
                URL = retArr2[7][z+1]   
        print('Ended this scrape') 
        
#===============================================================================
# Running main requires at a minimum a starting Book URL input and the number of authors and books to scrape. 
# Transferring this scraped data to the MongoDB database is handled after each scrape is finished.
# After all scraping and data is transferred, the optional arguments of exporting/importing JSON files will be handled.
#===============================================================================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = 'Parse a Book')
    parser.add_argument('Book_URL', type=str, help = "GoodReads Book URL")
    parser.add_argument('Number_Of_Books', type=int, help = "enter a number of books to scrape (between 1 and 200)")
    parser.add_argument('Number_Of_Authors', type=int, help = "enter a number of Authors to scrape (between 1 and 50)")
    parser.add_argument('-in' ,'--JSON_File_In', required = False, help = "enter a valid JSON File to read from")
    parser.add_argument('-existing' ,'--input', required = False, help = "enter a valid Book URL or Author URL to Export")
    parser.add_argument('-out' ,'--JSON_File_Out', required = False, help = "enter a JSON File to write to")

    args = parser.parse_args()
    
    if urlInRobotsFile(args.Book_URL):
        print("Warning! The given url is contained within the robots.txt file and should not be used") 
    
    if ('book' in args.Book_URL):
        if(args.Number_Of_Books > 200 and args.Number_Of_Authors > 50):
            print("Warning! Scraping more than 200 Books and 50 Authors can damage the scraped website")
            
        URL = args.Book_URL
        authorURL = runBookHandler(URL, args)
        runAuthorHandler(authorURL, args)
        readJson(args)
        writeJson(args)
    else:
        print('Invalid book URL. Must be a valid book URL from Goodreads.com')
     
    
    