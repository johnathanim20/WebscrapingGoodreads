"""
Implements the parser logic using regular expressions to handle speicifed commands in assignment2.1
"""
import argparse
import re
import pymongo
from database import get_key
from dns.rdataclass import NONE

def parseBeforeDot(string):
    """
    Helper function to parse string before a dot
    """
    try:
        find = re.compile(r"(.*?)\.")
        return re.search(find, string).group(1)
    except:
        return None
def parseAfterDot(string):
    """
    Helper function to parse string after a dot
    """
    try:
        find = re.compile(r"(?<=\.)(.*)")
        return (re.search(find, string).group(0))
    except:
        return None
def handleDotCommand(string, string2):
    """
    Helper function to handle a simple dot command
    """
    client = pymongo.MongoClient(get_key())
    data_base = client['GoodReadData']
    books = data_base["Books"]
    authors = data_base["Authors"]
    ret_arr1 = []
    if string2 == 'book':
        for book in books.find():
            ret_arr1.append(book[string])
    if string2 == 'author':
        for author in authors.find():
            ret_arr1.append(author[string])
    return ret_arr1, string2
def parseAfterColon(string):
    """
    Helper function to parse string after a colon
    """
    try:
        find = re.compile(r"(?<=:)(.*)")
        return (re.search(find, string).group(0))
    except:
        return None
def handleColonCommand(string, string2, search):
    """
    Helper function to handle a simple colon command
    """
    client = pymongo.MongoClient(get_key())
    data_base = client['GoodReadData']
    books = data_base["Books"]
    authors = data_base["Authors"]
    ret_arr1 = []
    if string2 == 'book':
        for book in books.find():
            if search in str(book[string]):
                print("The search value has been found at : " + book['book_url'])
                ret_arr1.append(book)
    elif string2 == 'author':
        for author in authors.find():
            if search in author[string]:
                print("The search value has been found at : " + author['author_url'])
                ret_arr1.append(author)
    return ret_arr1, string2
def handleNOTColonCommand(string, string2, search):
    """
    Helper function to handle a colon followed by a NOT command
    """
    client = pymongo.MongoClient(get_key())
    data_base = client['GoodReadData']
    books = data_base["Books"]
    authors = data_base["Authors"]
    ret_arr1 = []
    if string2 == 'book':
        for book in books.find():
            if search not in book[string]:
                print("The search value has not been found at : " + book['book_url'])
                ret_arr1.append(book[string])
        #print(ret_arr1)
    if string2 == 'author':
        for author in authors.find():
            if search not in author[string]:
                print("The search value has not been found at : " + author['author_url'])
                ret_arr1.append(author[string])
        #print(ret_arr2)
    return ret_arr1, string2
def parseAfterQuotes(string):
    """
    Helper function to parse string after a quote
    """
    try:
        find = re.compile(r"(?<=\')(.*)")
        return (re.search(find, string).group(0).strip("'"))
    except:
        return None
def handleQuotesCommand(string, string2, exact):
    """
    Helper function to handle a quotes command
    """
    client = pymongo.MongoClient(get_key())
    data_base = client['GoodReadData']
    books = data_base["Books"]
    authors = data_base["Authors"]
    ret_arr1 = []
    if string2 == 'book':
        for book in books.find():
            if book[string] == exact:
                print("The exact value has been found at : " + book['book_url'])
                ret_arr1.append(book[string])
    if string2 == 'author':
        for author in authors.find():
            if author[string] == exact:
                print("The exact value has been found at : " + author['author_url'])
                ret_arr1.append(author[string])
    return ret_arr1, string2
def handleNOTQuotesCommand(string, string2, exact):
    """
    Helper function to handle a quote followed by a NOT command
    """
    client = pymongo.MongoClient(get_key())
    data_base = client['GoodReadData']
    books = data_base["Books"]
    authors = data_base["Authors"]
    ret_arr1 = []
    if string2 == 'book':
        for book in books.find():
            if book[string] != exact:
                print("The exact value has not been found at : " + book['book_url'])
                ret_arr1.append(book[string])
    if string2 == 'author':
        for author in authors.find():
            if author[string] != exact:
                print("The exact value has not been found at : " + author['author_url'])
                ret_arr1.append(author[string])
    return ret_arr1, string2
def parseAfterAND(string):
    """
    Helper function to parse string after an AND
    """
    try:
        find = re.compile(r"(?<=AND)(.*)")
        return re.search(find, string).group(0)
    except:
        return None
def parseBeforeANDAfterColon(string):
    """
    Helper function to parse string before an AND and after a colon
    """
    try:
        find = re.findall('\:([^"]*)AND', string)[0]
        return find
    except:
        return None
def parseAfterNOT(string):
    """
    Helper function to parse string after a NOT
    """
    try:
        find = re.compile(r"(?<=NOT)(.*)")
        return re.search(find, string).group(1)
    except:
        return None

def parseAfterOR(string):
    """
    Helper function to parse string after an OR
    """
    try:
        find = re.compile(r"(?<=OR)(.*)")
        return re.search(find, string).group(0)
    except:
        return None
def parseBeforeORAfterColon(string):
    """
    Helper function to parse string before an OR and after a colon
    """
    try:
        find = re.findall('\:([^"]*)OR', string)[0]
        return find
    except:
        return None
def parseAfterGreaterThan(string):
    """
    Helper function to parse string after a >
    """
    try:
        find = re.compile(r"(?<=\>)(.*)")
        return re.search(find, string).group(0)
    except:
        return None
def handleGreaterThan(string, string2, value):
    """
    Helper function to handle a > command
    """
    if value.isdigit():
        client = pymongo.MongoClient(get_key())
        data_base = client['GoodReadData']
        books = data_base["Books"]
        authors = data_base["Authors"]
        ret_arr1 = []
        if string2 == 'book':
            for book in books.find():
                if book[string] > value:
                    print("A greater value than " + value +
                          " has been found at : " + book['book_url'])
                    ret_arr1.append(book[string])
        if string2 == 'author':
            for author in authors.find():
                if author[string] > value:
                    print("A greater value than " + value +
                          " has been found at : " + author['author_url'])
                    ret_arr1.append(author[string])
    return ret_arr1, string2
def parseAfterLessThan(string):
    """
    Helper function to parse string after a <
    """
    try:
        find = re.compile(r"(?<=\<)(.*)")
        return re.search(find, string).group(0)
    except:
        return None
def handleLessThan(string, string2, value):
    """
    Helper function to handle a < command
    """
    if value.isdigit():
        client = pymongo.MongoClient(get_key())
        data_base = client['GoodReadData']
        books = data_base["Books"]
        authors = data_base["Authors"]
        ret_arr1 = []
        if string2 == 'book':
            for book in books.find():
                if book[string] < value:
                    print("A lesser value than " + value +
                          " has been found at : " + book['book_url'])
                    ret_arr1.append(book[string])
        if string2 == 'author':
            for author in authors.find():
                if author[string] < value:
                    print("A lesser value than " + value +
                          " has been found at : " + author['author_url'])
                    ret_arr1.append(author[string])
    return ret_arr1, string2
def parseAfterDotBeforeColon(string):
    """
    Helper function to parse after a dot but before a colon
    """
    try:
        find = re.findall('\.([^"]*)\:', string)[0]
        return find
    except:
        return None
def dot(string):
    """
    Function to handle dot command
    """
    if '.' in string and parseAfterColon(string) is None:
        string1 = parseAfterDot(string)
        string2 = parseBeforeDot(string)
        return handleDotCommand(string1, string2)
def less_than(string):
    """
    Function to handle < command
    """
    if parseAfterColon(string) and parseAfterLessThan(string):
        string1 = parseBeforeDot(string)
        string2 = parseAfterDotBeforeColon(string)
        string3 = parseAfterLessThan(string)
        return handleLessThan(string2, string1, string3)
def greater_than(string):
    """
    Function to handle > command
    """
    if parseAfterColon(string) and parseAfterGreaterThan(string):
        string1 = parseBeforeDot(string)
        string2 = parseAfterDotBeforeColon(string)
        string3 = parseAfterGreaterThan(string)
        return handleGreaterThan(string2, string1, string3)
def and_colon(string):
    """
    Function to handle AND command with colon command
    """
    if (parseAfterColon(string) and parseBeforeANDAfterColon(string)
        and parseAfterQuotes(string) is None):
        string1 = parseBeforeANDAfterColon(string)
        string2 = parseAfterAND(string)
        string3 = parseBeforeDot(string)
        string4 = parseAfterDotBeforeColon(string)
        return handleColonCommand(string4, string3, string1)
        return handleColonCommand(string4, string3, string2)
def and_quotes(string):
    """
    Function to handle AND command with quotes
    """
    if (parseAfterQuotes(string) and parseBeforeANDAfterColon(string)
        and parseAfterQuotes(string)):
        string1 = parseBeforeANDAfterColon(string).strip("'")
        string2 = parseAfterAND(string).strip("'")
        string3 = parseBeforeDot(string)
        string4 = parseAfterDotBeforeColon(string)
        return handleQuotesCommand(string4, string3, string1)
        return handleQuotesCommand(string4, string3, string2)
def or_colon(string):
    """
    Function to handle OR command with colon
    """
    if (parseAfterColon(string) and parseAfterQuotes(string) is None
        and parseBeforeORAfterColon(string)):
        string1 = parseBeforeORAfterColon(string)
        string2 = parseAfterOR(string)
        string3 = parseBeforeDot(string)
        string4 = parseAfterDotBeforeColon(string)
        return handleColonCommand(string4, string3, string1)
        return handleColonCommand(string4, string3, string2)
def or_quotes(string):
    """
    Function to handle OR command with quotes
    """
    if (parseAfterColon(string) and parseAfterQuotes(string)
        and parseBeforeORAfterColon(string)):
        string1 = parseBeforeORAfterColon(string).strip("'")
        string2 = parseAfterOR(string).strip("'")
        string3 = parseBeforeDot(string)
        string4 = parseAfterDotBeforeColon(string)
        return handleQuotesCommand(string4, string3, string1)
        return handleQuotesCommand(string4, string3, string2)
def not_quote(string):
    """
    Function to handle NOT command with quotes
    """
    if (parseAfterColon(string) and parseAfterNOT(string)
        and parseAfterQuotes(string)):
        string1 = parseAfterQuotes(string)
        string2 = parseBeforeDot(string)
        string3 = parseAfterDotBeforeColon(string)
        return handleNOTQuotesCommand(string3, string2, string1)
def not_colon(string):
    """
    Function to handle NOT command with colon
    """
    if parseAfterColon(string) and parseAfterNOT(string):
        string1 = parseAfterNOT(string)
        string2 = parseBeforeDot(string)
        string3 = parseAfterDotBeforeColon(string)
        return handleNOTColonCommand(string3, string2, string1)
def quote(string):
    """
    Function to handle quotes command
    """
    if parseAfterColon(string) and parseAfterQuotes(string):
        string1 = parseAfterQuotes(string)
        string2 = parseBeforeDot(string)
        string3 = parseAfterDotBeforeColon(string)
        return handleQuotesCommand(string3, string2, string1)
def colon(string):
    """
    Function to handle colon command
    """
    if (parseAfterColon(string) and parseAfterQuotes(string) is None
        and parseAfterAND(string) is None and parseAfterLessThan(string) is None
        and parseAfterLessThan(string) is None):
        string1 = parseAfterColon(string)
        string2 = parseBeforeDot(string)
        string3 = parseAfterDotBeforeColon(string)
        return handleColonCommand(string3, string2, string1)
def main():
    """
    Main function used to test if the parsing works as expected.
    """
    parser = argparse.ArgumentParser(description = 'Parse user Input')
    parser.add_argument('operator', help = "Must use a valid operator")
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
    elif (parseAfterColon(args.operator)and parseBeforeANDAfterColon(args.operator)
          and parseAfterQuotes(args.operator) is None):
        string1 = parseBeforeANDAfterColon(args.operator)
        string2 = parseAfterAND(args.operator)
        string3 = parseBeforeDot(args.operator)
        string4 = parseAfterDotBeforeColon(args.operator)
        handleColonCommand(string4, string3, string1)
        handleColonCommand(string4, string3, string2)
    #handles a simple AND operation of Quote commands
    elif (parseAfterQuotes(args.operator) and parseBeforeANDAfterColon(args.operator)
          and parseAfterQuotes(args.operator)):
        string1 = parseBeforeANDAfterColon(args.operator).strip("'")
        string2 = parseAfterAND(args.operator).strip("'")
        string3 = parseBeforeDot(args.operator)
        string4 = parseAfterDotBeforeColon(args.operator)
        handleQuotesCommand(string4, string3, string1)
        handleQuotesCommand(string4, string3, string2)
    elif (parseAfterColon(args.operator) and parseAfterQuotes(args.operator) is None
          and parseBeforeORAfterColon(args.operator)):
    #handles a simple OR operation of colon commands
        string1 = parseBeforeORAfterColon(args.operator)
        string2 = parseAfterOR(args.operator)
        string3 = parseBeforeDot(args.operator)
        string4 = parseAfterDotBeforeColon(args.operator)
        print(string1,string2,string3,string4)
        handleColonCommand(string4, string3, string1)
        handleColonCommand(string4, string3, string2)
    elif (parseAfterColon(args.operator) and parseAfterQuotes(args.operator)
          and parseBeforeORAfterColon(args.operator)):
    #handles a simple OR operation of quote commands
        string1 = parseBeforeORAfterColon(args.operator).strip("'")
        string2 = parseAfterOR(args.operator).strip("'")
        string3 = parseBeforeDot(args.operator)
        string4 = parseAfterDotBeforeColon(args.operator)
        handleQuotesCommand(string4, string3, string1)
        handleQuotesCommand(string4, string3, string2)
    elif (parseAfterColon(args.operator) and parseAfterNOT(args.operator)
          and parseAfterQuotes(args.operator)):
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
    elif (parseAfterColon(args.operator) and parseAfterQuotes(args.operator) is None
          and parseAfterAND(args.operator) is None and parseAfterLessThan(args.operator) is None
            and parseAfterLessThan(args.operator) is None):
    #handles a '.' operation followed by a colon operation
        string1 = parseAfterColon(args.operator)
        string2 = parseBeforeDot(args.operator)
        string3 = parseAfterDotBeforeColon(args.operator)
        handleColonCommand(string3, string2, string1)
if __name__ == "__main__":
    main()
