from calendar import c
import requests
from bs4 import BeautifulSoup
import csv
import re

booksonline_url = "https://books.toscrape.com/catalogue/category/books_1/index.html"

def parse_html(booksonline_url):
    """ Extraire le contenu de la page html du site booksonline"""

    page_response = requests.get(booksonline_url)
    return BeautifulSoup(page_response.content, 'html.parser')

def next_page_category(category_url):
    """ Détecter la présence d'un tag next par catégorie"""

    content = parse_html(category_url)
    next_page_tag = content.find('li', class_="next")  
    return next_page_tag

def extract_categories_urls(category_url):
    """ Extraire les URLS des pages de chaque catégorie en détectant la présence du bouton next """
    
    pages_categories_url = [category_url]
    response_category = requests.get(category_url)
    soup_category = BeautifulSoup(response_category.content, 'html.parser')
    page_url_processed = category_url.replace("index.html", "")
    page_number = 2

    while True:
        nextpage_tag = soup_category.find('li', class_="next")
        if nextpage_tag is None:
            break
        page_url = f'{page_url_processed}page-{page_number}.html'
        pages_categories_url.append(page_url)
        response_category = requests.get(page_url)
        soup_category = BeautifulSoup(response_category.content, 'html.parser')
        page_number += 1

    return pages_categories_url

def extract_books_urls(categories_urls):
    """ Extraire les URLS de tous les livres par catégorie"""

    books_url = []
    for page_url in categories_urls:
        content = parse_html(page_url)
        titles = content.find_all("h3")
        for title in titles:
            tag_href = title.find('a')["href"]
            url = tag_href.replace("../../../", "http://books.toscrape.com/catalogue/")
            books_url.append(url)

    return books_url

def extract_book_data(url):
    """Extraire les data d'un livre"""

    book_url = url
    url = parse_html(url)
    book_data = {}

    book_data['product_page_url'] = book_url
    book_data['universal_product_codes'] = url.find("table", class_="table table-striped").findAll("td")[0].text
    book_data['title'] = url.find("h1").text
    book_data['price_including_tax'] = url.find("table", class_="table table-striped").findAll("td")[3].text.lstrip("Â£")
    book_data['price_excluding_tax'] = url.find("table", class_="table table-striped").findAll("td")[2].text.lstrip("Â£")
    number_available_tag = url.find("table", class_="table table-striped").findAll("td")[5].text
    number_available_tag = re.sub(r'\D', '', str(number_available_tag))
    number_available_tag = int(number_available_tag)
    book_data['number_available'] = number_available_tag
    book_data['product_description'] = url.findAll('p')[3].text
    book_data['category'] = url.find('ul', class_="breadcrumb").findAll('a')[2].text
    book_data['review_rating'] = url.findAll("p", class_="star-rating")[0]['class'][1] 
    book_data['image_url'] = url.findAll('img')[0]['src'].replace("../..", "http://books.toscrape.com") 

    return book_data

if __name__ == '__main__':
   book_data = extract_book_data("https://books.toscrape.com/catalogue/someone-like-you-the-harrisons-2_735/index.html")
   print(book_data)

