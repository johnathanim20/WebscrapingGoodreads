import argparse
import re
import pymongo
from database import get_key
from dns.rdataclass import NONE

def parseBeforeDot(string):
    try:
        find = re.compile(r"(.*?)\.")
        return re.search(find, string).group(1)
    except:
        return None
def parseAfterDot(string):
    try:
        find = re.compile(r"(?<=\.)(.*)")
        return (re.search(find, string).group(0))
    except:
        return None
def handleDotCommand(string, string2):
    client = pymongo.MongoClient(get_key())
    data_base = client['GoodReadData']
    books = data_base["Books"]
    authors = data_base["Authors"]
    ret_arr1 = []
    ret_arr2 = []
    if (string2 == 'book'):
        for book in books.find():   
            ret_arr1.append(book[string])
        print(ret_arr1)
    if (string2 == 'author'):
        for author in authors.find():
            ret_arr2.append(author[string])
        print(ret_arr2)

def parseAfterColon(string):
    try:
        find = re.compile(r"(?<=:)(.*)")
        return (re.search(find, string).group(0))
    except:
        return None
    
def handleColonCommand(string, string2, search):
    client = pymongo.MongoClient(get_key())
    data_base = client['GoodReadData']
    books = data_base["Books"]
    authors = data_base["Authors"]
    ret_arr1 = []
    if (string2 == 'book'):
        for book in books.find():
            if search in book[string]:
                print("The search value has been found at : " + book['book_url'])
                ret_arr1.append(book)
        
    elif (string2 == 'author'):  
        for author in authors.find():
            if search in author[string]:
                print("The search value has been found at : " + author['author_url'])
                ret_arr1.append(author)
        
    return ret_arr1, string2
def handleNOTColonCommand(string, string2, search):
    client = pymongo.MongoClient(get_key())
    data_base = client['GoodReadData']
    books = data_base["Books"]
    authors = data_base["Authors"]
    ret_arr1 = []
    ret_arr2 = []
    if (string2 == 'book'):
        for book in books.find():   
            
            if search not in book[string]:
                print("The search value has not been found at : " + book['book_url'])
                ret_arr1.append(book[string])
        #print(ret_arr1)
    if (string2 == 'author'):  
        for author in authors.find():
            if search not in author[string]:
                print("The search value has not been found at : " + author['author_url'])
                ret_arr2.append(author[string])
        #print(ret_arr2)

def parseAfterQuotes(string):
    try:
        find = re.compile(r"(?<=\')(.*)")
        return (re.search(find, string).group(0).strip("'"))
    except:
        return None    
def handleQuotesCommand(string, string2, exact):
    client = pymongo.MongoClient(get_key())
    data_base = client['GoodReadData']
    books = data_base["Books"]
    authors = data_base["Authors"]
    ret_arr1 = []
    ret_arr2 = []
    if (string2 == 'book'):
        for book in books.find():   
            if book[string] == exact:
                print("The exact value has been found at : " + book['book_url'])
                ret_arr1.append(book[string])      
    if (string2 == 'author'):  
        for author in authors.find():
            if author[string] == exact:
                print("The exact value has been found at : " + author['author_url']) 
                ret_arr2.append(author[string])
def handleNOTQuotesCommand(string, string2, exact):
    client = pymongo.MongoClient(get_key())
    data_base = client['GoodReadData']
    books = data_base["Books"]
    authors = data_base["Authors"]
    ret_arr1 = []
    ret_arr2 = []
    if (string2 == 'book'):
        for book in books.find():   
            if book[string] != exact:
                print("The exact value has not been found at : " + book['book_url'])
                ret_arr1.append(book[string])
    if (string2 == 'author'):  
        for author in authors.find():
            if author[string] != exact:
                print("The exact value has not been found at : " + author['author_url']) 
                ret_arr2.append(author[string])
        
def parseAfterAND(string):
    try:
        find = re.compile(r"(?<=AND)(.*)")
        return re.search(find, string).group(0)
    except:
        return None
def parseBeforeANDAfterColon(string):
    try:
        find = re.findall('\:([^"]*)AND', string)[0]
        return find
    except:
        return None
def parseAfterNOT(string):
    try:
        find = re.compile(r"(?<=NOT)(.*)")
        return re.search(find, string).group(1)
    except:
        return None

def parseAfterOR(string):
    try:
        find = re.compile(r"(?<=OR)(.*)")
        return re.search(find, string).group(0)
    except:
        return None
def parseBeforeORAfterColon(string):
    try:
        find = re.findall('\:([^"]*)OR', string)[0]
        return find
    except:
        return None
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
    try:
        find = re.compile(r"(?<=\>)(.*)")
        return re.search(find, string).group(0)
    except:
        return None
def handleGreaterThan(string, string2, value):
    if value.isdigit():
        client = pymongo.MongoClient(get_key())
        data_base = client['GoodReadData']
        books = data_base["Books"]
        authors = data_base["Authors"]
        ret_arr1 = []
        ret_arr2 = []
        
        if (string2 == 'book'):
            for book in books.find():   
                if book[string] > value:
                    print("A greater value than " + value + " has been found at : " + book['book_url'])
                    ret_arr1.append(book[string])
        if (string2 == 'author'):  
            for author in authors.find():
                if author[string] > value:
                    print("A greater value than " + value + " has been found at : " + author['author_url'])
                    ret_arr2.append(author[string])
        

def parseAfterLessThan(string):
    try:
        find = re.compile(r"(?<=\<)(.*)")
        return re.search(find, string).group(0)
    except:
        return None
    
    
def handleLessThan(string, string2, value):
    if value.isdigit():
        client = pymongo.MongoClient(get_key())
        data_base = client['GoodReadData']
        books = data_base["Books"]
        authors = data_base["Authors"]
        ret_arr1 = []
        ret_arr2 = []
        
        if (string2 == 'book'):
            for book in books.find():   
                if book[string] < value:
                    print("A lesser value than " + value + " has been found at : " + book['book_url'])
                    ret_arr1.append(book[string])
        if (string2 == 'author'):  
            for author in authors.find():
                if author[string] < value:
                    print("A lesser value than " + value + " has been found at : " + author['author_url'])
                    ret_arr2.append(author[string])

def parseAfterDotBeforeColon(string):
    try:
        find = re.findall('\.([^"]*)\:', string)[0]
        return find
    except:
        return None
def main():
    parser = argparse.ArgumentParser(description = 'Parse user Input')
    parser.add_argument('operator', help = "Must use a valid operator containing : '., :, "", AND, OR, NOT, <, >")
    args = parser.parse_args()
    #handles a simple '.' operation
    if '.' in args.operator and parseAfterColon(args.operator) is None:
        string1 = parseAfterDot(args.operator)
        string2 = parseBeforeDot(args.operator)
        handleDotCommand(string1, string2)
    #handles a less than operation
    elif parseAfterColon(args.operator) and parseAfterLessThan(args.operator):
        string1 = parseBeforeDot(args.operator)
        string2 = parseAfterDotBeforeColon(args.operator)
        string3 = parseAfterLessThan(args.operator)
        handleLessThan(string2, string1, string3)
    #handles a greater than operation
    elif parseAfterColon(args.operator) and parseAfterGreaterThan(args.operator):
        string1 = parseBeforeDot(args.operator)
        string2 = parseAfterDotBeforeColon(args.operator)
        string3 = parseAfterGreaterThan(args.operator)
        handleGreaterThan(string2, string1, string3)
    #handles a simple AND operation of colon commands  
    elif parseAfterColon(args.operator) and parseBeforeANDAfterColon(args.operator) and parseAfterQuotes(args.operator) is None:
        string1 = parseBeforeANDAfterColon(args.operator)
        string2 = parseAfterAND(args.operator)
        string3 = parseBeforeDot(args.operator)
        string4 = parseAfterDotBeforeColon(args.operator)
        handleColonCommand(string4, string3, string1)
        handleColonCommand(string4, string3, string2)
    #handles a simple AND operation of Quote commands     
    elif parseAfterQuotes(args.operator) and parseBeforeANDAfterColon(args.operator) and parseAfterQuotes(args.operator):
        string1 = parseBeforeANDAfterColon(args.operator).strip("'")
        string2 = parseAfterAND(args.operator).strip("'")
        string3 = parseBeforeDot(args.operator)
        string4 = parseAfterDotBeforeColon(args.operator)
        handleQuotesCommand(string4, string3, string1)
        handleQuotesCommand(string4, string3, string2)
    elif parseAfterColon(args.operator) and parseAfterQuotes(args.operator) is None and parseBeforeORAfterColon(args.operator):
    #handles a simple OR operation of colon commands
        string1 = parseBeforeORAfterColon(args.operator)
        string2 = parseAfterOR(args.operator)
        string3 = parseBeforeDot(args.operator)
        string4 = parseAfterDotBeforeColon(args.operator)
        print(string1,string2,string3,string4)
        handleColonCommand(string4, string3, string1)
        handleColonCommand(string4, string3, string2)
    elif parseAfterColon(args.operator) and parseAfterQuotes(args.operator) and parseBeforeORAfterColon(args.operator):
    #handles a simple OR operation of quote commands
        string1 = parseBeforeORAfterColon(args.operator).strip("'")
        string2 = parseAfterOR(args.operator).strip("'")
        string3 = parseBeforeDot(args.operator)
        string4 = parseAfterDotBeforeColon(args.operator)
        handleQuotesCommand(string4, string3, string1)
        handleQuotesCommand(string4, string3, string2)
    elif parseAfterColon(args.operator) and parseAfterNOT(args.operator) and parseAfterQuotes(args.operator):
    #handles a '.' operation followed by a colon, NOT, and Quotes operation.  
        string1 = parseAfterQuotes(args.operator)
        string2 = parseBeforeDot(args.operator)
        string3 = parseAfterDotBeforeColon(args.operator)
        handleNOTQuotesCommand(string3, string2, string1)
    elif parseAfterColon(args.operator) and parseAfterNOT(args.operator):
    #handles a '.' operation followed by a colon and NOT operation
        string1 = parseAfterNOT(args.operator)
        string2 = parseBeforeDot(args.operator)
        string3 = parseAfterDotBeforeColon(args.operator)
        handleNOTColonCommand(string3, string2, string1) 
    elif parseAfterColon(args.operator) and parseAfterQuotes(args.operator): 
    #handles a '.' operation followed by a colon and Quotes operation
        string1 = parseAfterQuotes(args.operator)
        string2 = parseBeforeDot(args.operator)
        string3 = parseAfterDotBeforeColon(args.operator)
        handleQuotesCommand(string3, string2, string1)
    elif (parseAfterColon(args.operator) and parseAfterQuotes(args.operator) is None and parseAfterAND(args.operator) is None and parseAfterLessThan(args.operator) is None 
            and parseAfterLessThan(args.operator) is None):
    #handles a '.' operation followed by a colon operation
        string1 = parseAfterColon(args.operator)
        string2 = parseBeforeDot(args.operator)
        string3 = parseAfterDotBeforeColon(args.operator)
        handleColonCommand(string3, string2, string1)
    
 
if __name__ == "__main__":
    main()
        

