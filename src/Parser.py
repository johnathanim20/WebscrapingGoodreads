import argparse
import re
import pymongo
from database import get_key
def parseAfterDot(string):
    find = re.compile(r"(?<=\.)(.*)")
    return (re.search(find, string).group(0))

def handleDotCommand(string):
    client = pymongo.MongoClient(get_key())
    data_base = client['GoodReadData']
    books = data_base["Books"]
    authors = data_base["Authors"]
    ret_arr1 = []
    ret_arr2 = []
    for book in books.find():   
        ret_arr1.append(book[string])
    for author in authors.find():
        ret_arr2.append(author[string])
    print(ret_arr1)
    print(ret_arr2)

def parseAfterColon(string):
    find = re.compile(r"(?<=:)(.*)")
    return (re.search(find, string).group(0))

def handleColonCommand(string, search):
    client = pymongo.MongoClient(get_key())
    data_base = client['GoodReadData']
    books = data_base["Books"]
    authors = data_base["Authors"]
    ret_arr1 = []
    ret_arr2 = []
    for book in books.find():   
        if search in book[string]:
            print("The search value has been found at : " + book['book_url'])
        ret_arr1.append(book[string])
    for author in authors.find():
        if search in author[string]:
            print("The search value has been found at : " + author['author_url'])
        ret_arr2.append(author[string])

def parseAfterQuotes(string):
    find = re.findall('"([^"]*)"', string)[0]
    return find

def handleQuotesCommand(string, exact):
    client = pymongo.MongoClient(get_key())
    data_base = client['GoodReadData']
    books = data_base["Books"]
    authors = data_base["Authors"]
    ret_arr1 = []
    ret_arr2 = []
    for book in books.find():   
        if book[string] == exact:
            print("The exact value has been found at : " + book['book_url'])
            return True
        ret_arr1.append(book[string])
    for author in authors.find():
        if author[string] == exact:
            print("The exact value has been found at : " + author['author_url'])
            return True
        ret_arr2.append(author[string])
        
def parseAfterAND(string):
    find = re.compile(r"(?<=AND )(.*)")
    return re.search(find, string).group(0)
    
def parseBeforeAND(string):
    find = re.compile(r"(.*?)AND")
    return re.search(find, string).group(1)

def handleANDCommand(string1, string2, exact, search):
    #if quotes 
    if handleQuotesCommand(string1, exact) and handleQuotesCommand(string2, exact):
        return True
    #if Colons
    if handleColonCommand(string1, search) and handleColonCommand(string2, search):
        return True
    #if Dots
    if handleDotCommand(string1) and handleDotCommand(string2):
        return True
    
def parseAfterNOT(string):
    find = re.compile(r"(?<=NOT )(.*)")
    return re.search(find, string).group(0)

def handleNOTCommand(string, exact, search):
    #if quotes
    if not handleQuotesCommand(string, exact):
        return False
    #if Colons
    if not handleColonCommand(string, search):
        return False
    #if Dots
    if not handleDotCommand(string):
        return False

def parseBeforeOR(string):
    find = re.compile(r"(.*?)OR")
    return re.search(find, string).group(1)

def parseAfterOR(string):
    find = re.compile(r"(?<=OR )(.*)")
    return re.search(find, string).group(0)

def handleORCommand(string1, string2, exact, search):
    #if quotes 
    if handleQuotesCommand(string1, exact) or handleQuotesCommand(string2, exact):
        return True
    #if Colons
    if handleColonCommand(string1, search) or handleColonCommand(string2, search):
        return True
    #if Dots
    if handleDotCommand(string1) or handleDotCommand(string2):
        return True
    
def parseAfterGreaterThan(string):
    find = re.compile(r"(?<=\<)(.*)")
    return re.search(find, string).group(0)

def handleGreaterThan(string, value):
    client = pymongo.MongoClient(get_key())
    data_base = client['GoodReadData']
    books = data_base["Books"]
    authors = data_base["Authors"]
    ret_arr1 = []
    ret_arr2 = []
    for book in books.find():   
        ret_arr1.append(book[string])
    for author in authors.find():
        ret_arr2.append(author[string])
    new_arr1 = []
    new_arr2 = []
    for x in range(len(ret_arr1)):
        if (value > book[string]):
            new_arr1.append(book[string])
    for x in range(len(ret_arr2)):
        if (value > author[string]):
            new_arr2.append(authors[string])   
    return new_arr1, new_arr2

def parseAfterLessThan(string):
    find = re.compile(r"(?<=\<)(.*)")
    return re.search(find, string).group(0)

def handleLessThan(string, value):
    client = pymongo.MongoClient(get_key())
    data_base = client['GoodReadData']
    books = data_base["Books"]
    authors = data_base["Authors"]
    ret_arr1 = []
    ret_arr2 = []
    for book in books.find():   
        ret_arr1.append(book[string])
    for author in authors.find():
        ret_arr2.append(author[string])
    new_arr1 = []
    new_arr2 = []
    for x in range(len(ret_arr1)):
        if (value < book[string]):
            new_arr1.append(book[string])
    for x in range(len(ret_arr2)):
        if (value < author[string]):
            new_arr2.append(authors[string])   
    return new_arr1, new_arr2
def main():
    #===========================================================================
    # parser = argparse.ArgumentParser(description = 'Parse user Input')
    # parser.add_argument('operator', help = "Must use a valid operator containing : '., :, "", AND, OR, NOT, <, >")
    # args = parser.parse_args()
    # if (Operator in args.operator):
    #===========================================================================
    handleDotCommand()
if __name__ == "__main__":
    main()
        

