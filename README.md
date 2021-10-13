# fa21-cs242-assignment-2
The project : fa21-cs242-assignment-2 consists of 3 different python   
modules that include functions to take care of many of the core functionalities  
of web scraping, transferring data to an external database, and also handling the usage   
of a command line interface so that a user can export or import JSON data.  
The Scraper Python Module handles the actual logic behind the scraping and parsing of website data  
by using the inspect element function on the GoodReads.com website to find common attributes  
that are shared between books and authors. The Database Python Module handles the transferring of data  
that has been retrieved using the Scraper Module and utilizes MongoDB's cloud services to store data.  
The CommandLine module is where the program sets up the command line interface for a user to interact with     
and give valid inputs. The user should always supply at a minimum a starting book URL and the number of authors   
and books to scrape. There is a also a test module that checks if helper functions used for the base functionality  
are working as expected. Part 1 of this project has been completed as of 9/26/21.
