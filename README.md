# Scraping the website Books to scrape

The purpose of the program is to extract a .csv file for each category of books as well as the images of each book : http://books.toscrape.com/catalogue/category/books_1/index.html

Below, you will find the different information scraped by the program: 
1) product_page_url
2) universal_product_code
3) price_including_tax
4) number_avalaible
5) category
6) review_rating
7) image_url

## Getting Started

### Prerequisites

Install Python 3.11: https://www.python.org/

Install Request:  python3.11 -m pip install requests

Instal BeautifulSoup: python3.11 -m pip install beautifulsoup4

#### Installing

- git clone : https://github.com/hugohlr13/OCRP2.git
- Open the terminal.
- Create the virtual environment: python -m venv env
- Install Requireemnts: pip install -r requirements.txt 
- Activate the virtual environment:  source env/bin/activate

## Running the tests

- Position in the folder created bookstoscrape.
- Use the command : python3 booksonline.py 
- Wait for the script to finish creating the folders books_data and books_images with the desired files.

## Author

Hugo Huet-Leroy
hugo.huetleroy@gmail.com







