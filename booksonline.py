import requests
from bs4 import BeautifulSoup
import csv

# lien de la page à scrapper
url = "http://books.toscrape.com/catalogue/tipping-the-velvet_999/index.html"
reponse = requests.get(url)
page = reponse.content

# transforme (parse) le HTML en objet BeautifulSoup
soup = BeautifulSoup(page, "html.parser")

# extraction des données d'un produit :

product_page_url = url
print(product_page_url)

universal_product_code = soup.find("table", class_="table table-striped").findAll("td")[0].string
print(universal_product_code)

title = soup.find("h1").string
print (title)

price_including_tax = soup.find("table", class_="table table-striped").findAll("td")[3].string
print(price_including_tax)

price_excluding_tax = soup.find("table", class_="table table-striped").findAll("td")[2].string
print(price_excluding_tax)

number_avalaible = soup.find("table", class_="table table-striped").findAll("td")[5].string
print(number_avalaible)

product_description = soup.findAll("p")[3].string
print(product_description)

category = soup.find("ul", class_="breadcrumb").findAll("a")[2].string
print(category)

review_rating = soup.findAll("p", class_="star-rating")[0]["class"][1]
print(review_rating)

image_url = soup.findAll('img')[0]['src'].replace("../..", "http://books.toscrape.com")
print(image_url)

# stockage des données dans un fichier local .csv :

en_tete = ['product_page_url', 'universal_product_code', 'title', 'price_including_tax', 'price_excluding_tax', 'number_avalaible', 'product_description', 'category', 'review_rating', 'image_url']
with open('databooksonline.csv', 'w') as csv_file:
    writer = csv.writer(csv_file, delimiter=',')
    writer.writerow(en_tete)
    writer.writerow([product_page_url, universal_product_code, title, price_including_tax, price_excluding_tax, number_avalaible, product_description, category, review_rating, image_url])

