import requests
from bs4 import BeautifulSoup
import csv

# lien de la page à scrapper
	url = "http://books.toscrape.com/catalogue/tipping-the-velvet_999/index.html"
	reponse = requests.get(url)
	page = reponse.content

# transforme (parse) le HTML en objet BeautifulSoup
	soup = BeautifulSoup(page, "html.parser")


# récupération de toutes les informations :

# universal_product_code (upc)
	universal_product_code = soup.find("td[0]", class_="table table-striped")


