# Centos Scraper
Machine Problem: Web Scraping

A python application which  scrape all of the filenames, download links and filesizes  in all of the inside pages of http://mirror.rise.ph/centos/7/

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

First you need to install the requests package and BeautifulSoup4 package

#### Install using pipenv 

```
pipenv install requests BeautifulSoup4
```

## To Use

type in the command line your Github username, password, and the term you want to search

####Example:
```
python search.py (term) -u (username) -p (password)

#if you forgot your password a prompt will show to input your password
python search.py (term) -u (username)
Github Password:
#the input password will not echo in the stdout so it is more secure
```

The result will be saved on a CSV file with a file name of output-YYYY-MM-DD-HH-mm.csv

## Author
**Johnzel Tuddao** - *Initial work* - [J0hnZMT](https://github.com/J0hnZMT)

## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

