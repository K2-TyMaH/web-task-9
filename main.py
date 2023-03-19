from pprint import pprint
import json
from datetime import datetime

import requests
from bs4 import BeautifulSoup


base_url = "http://quotes.toscrape.com"


def get_parsed_urls() -> list:
    urls = []
    for i in range(10):
        suffix = f"/page/{i+1}/"
        urls.append(base_url + suffix)
    return urls


def get_authors_urls(urls: list) -> set:
    authors = set()
    for url in urls:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        author_urls = soup.find_all('div', class_='quote')
        for author_url in author_urls:
            authors.add(author_url.find('a').get('href'))
    return authors


def authors_spider(author_urls: set) -> list:
    authors_info = []
    for url in author_urls:
        response = requests.get(base_url + url)
        soup = BeautifulSoup(response.text, 'lxml')
        fullname = soup.find('h3', class_='author-title').text.strip()
        born_date = soup.find('span', class_='author-born-date').text.strip()
        born_location = soup.find('span', class_='author-born-location').text.strip()
        description = soup.find('div', class_='author-description').text.strip()
        authors_info.append({'fullname': fullname, 'born_date': born_date, 'born_location': born_location,
                             'description': description})

    return authors_info


def quotes_spider(parsed_urls: list) -> list:
    quotes_info = []
    for url in parsed_urls:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        quotes = soup.find_all('span', class_='text')
        authors = soup.find_all('small', class_='author')
        tags = soup.find_all('div', class_='tags')
        for i in range(0, len(quotes)):
            quote = quotes[i].text.strip()
            author = authors[i].text.strip()
            tags_html = tags[i].find_all('a', class_='tag')
            tags_list = []
            for tag in tags_html:
                tags_list.append(tag.text.strip())
            quotes_info.append({'tags': tags_list, 'author': author, 'quote': quote})

    return quotes_info


if __name__ == '__main__':
    urls_for_parser = get_parsed_urls()
    quotes = quotes_spider(urls_for_parser)
    with open('quotes.json', 'w', encoding='utf-8') as fd:
        json.dump(quotes, fd, ensure_ascii=False)
    authors = authors_spider(get_authors_urls(urls_for_parser))
    with open('authors.json', 'w', encoding='utf-8') as fd:
        json.dump(authors, fd, ensure_ascii=False)

