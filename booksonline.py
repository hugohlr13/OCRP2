from pathlib import Path
import requests
from bs4 import BeautifulSoup
import csv
import re

booksonline_url = "https://books.toscrape.com/catalogue/category/books_1/index.html"

def parse_html(booksonline_url):
    """ Extraire le contenu de la page html du site booksonline"""

    page_response = requests.get(booksonline_url)
    return BeautifulSoup(page_response.content, 'html.parser')

def extract_category_urls(booksonline_url):
    """ Obtenir les URL de chaque catégorie"""

    content = parse_html(booksonline_url)
    category_tags = content.findAll("ul")[2].findAll("a")
    
    category_href = []
    for category_unprocessed in category_tags:
        category_href.append(category_unprocessed["href"])
    
    category_urls = []
    for first_page in category_href:
        first_page_category = first_page.replace("../", "")
        category_urls.append("http://books.toscrape.com/catalogue/category/" + first_page_category)
    
    return category_urls

def extract_pages_category_urls(category_urls):
    """ Extraire les URLS des pages de chaque catégorie en détectant la présence du bouton next """
    
    pages_category_urls = [category_urls]
    content = parse_html(category_urls)
    page_url_processed = category_urls.replace("index.html", "")
    page_number = 2

    while True:
        nextpage_tag = content.find('li', class_="next")
        if nextpage_tag is None:
            break
        page_url = f'{page_url_processed}page-{page_number}.html'
        pages_category_urls.append(page_url)
        content = parse_html(page_url)
        page_number += 1

    return pages_category_urls

def extract_books_urls(pages_category_urls):
    """ Extraire les URLS de tous les livres par catégorie"""

    books_urls = []
    for page_url in pages_category_urls:
        content = parse_html(page_url)
        titles = content.find_all("h3")
        for title in titles:
            tag_href = title.find('a')["href"]
            url = tag_href.replace("../../../", "http://books.toscrape.com/catalogue/")
            books_urls.append(url)

    return books_urls

def extract_book_data(book_url):
    """Extraire les data d'un livre"""

    url = book_url
    book_url = parse_html(book_url)
    book_data = {}

    book_data['product_page_url'] = url
    book_data['universal_product_codes'] = book_url.find("table", class_="table table-striped").findAll("td")[0].text
    book_data['title'] = book_url.find("h1").text
    book_data['price_including_tax'] = book_url.find("table", class_="table table-striped").findAll("td")[3].text.lstrip("Â£")
    book_data['price_excluding_tax'] = book_url.find("table", class_="table table-striped").findAll("td")[2].text.lstrip("Â£")
    number_available_tag = book_url.find("table", class_="table table-striped").findAll("td")[5].text
    number_available_tag = re.sub(r'\D', '', str(number_available_tag))
    number_available_tag = int(number_available_tag)
    book_data['number_available'] = number_available_tag
    book_data['product_description'] = book_url.findAll('p')[3].text
    book_data['category'] = book_url.find('ul', class_="breadcrumb").findAll('a')[2].text
    book_data['review_rating'] = book_url.findAll("p", class_="star-rating")[0]['class'][1] 
    book_data['image_url'] = book_url.findAll('img')[0]['src'].replace("../..", "http://books.toscrape.com") 

    return book_data

def extract_books_data(books_urls):
    """ Extraire les data des livres d'une catégorie"""
    return [extract_book_data(book_url) for book_url in books_urls]

def load_csv_category(books_data):
    """ Sauvegarder les data des livres d'une catégorie"""

    category_name = books_data[0]["category"]
    folder_path = Path("books_data") / category_name
    folder_path.mkdir(parents=True, exist_ok=True)

    file_path = folder_path / f"{category_name}.csv"

    en_tete = ['product_page_url', 'universal_product_code', 'title', 'price_including_tax', 'price_excluding_tax', 'number_avalaible', 'product_description', 'category', 'review_rating', 'image_url']

    with open(file_path, "w") as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(en_tete)
        for book_data in books_data:
            writer.writerow([book_data['product_page_url'], book_data['universal_product_codes'], book_data['title'], book_data['price_including_tax'], book_data['price_excluding_tax'], book_data['number_available'], book_data['product_description'], book_data['category'], book_data['review_rating'], book_data['image_url']])

def load_books_images(books_data):
    """ Sauvegarder les images des livres par catégorie"""

    category_name = books_data[0]["category"]
    folder_path = Path("books_images") / category_name 
    folder_path.mkdir(parents=True, exist_ok=True)

    for book_data in books_data:
        print(book_data['image_url'], book_data['title'])
        image = requests.get(book_data['image_url']).content
        title_format = ''.join(char for char in book_data['title'] if char.isalnum())
        file_path = folder_path / f"{title_format}.jpg"
        print(file_path)
        with open(file_path, "wb") as image_file:
            image_file.write(image)

def etl():
    """ Enregistrer dans un fichier .csv les informations des livres par catégorie et enregistrer les images de tous les livres en local """

    booksonline_url = "https://books.toscrape.com/catalogue/category/books_1/index.html"
    category_urls = extract_category_urls(booksonline_url)
    print(category_urls)
    for category_url in category_urls:
        pages_category_urls = extract_pages_category_urls(category_url)
        print(pages_category_urls)
        books_urls = extract_books_urls(pages_category_urls)
        print(books_urls)
        print(len(books_urls))
        books_data = extract_books_data(books_urls)
        print(books_data)
        load_csv_category(books_data)
        load_books_images(books_data)


if __name__ == '__main__':
    etl()
