from bs4 import BeautifulSoup
import requests
import re
import pyrebase
import datetime
import json
import hashlib

pyrebase_config = {
  "apiKey": "AIzaSyCKh0Rg_sQuFH83Ev4eTZ4TxLYYQ2ui59w",
  "authDomain": "scrappy-896fd.firebaseapp.com",
  "databaseURL": "https://scrappy-896fd.firebaseio.com",
  "storageBucket": "scrappy-896fd.appspot.com"
}

firebase = pyrebase.initialize_app(pyrebase_config)

# Get a reference to the database service
db = firebase.database()

# iphones = 'https://www.amazon.fr/s?i=electronics&bbn=218193031&rh=n%3A13921051%2Cn%3A13910671%2Cn%3A14060661%2Cn%3A218193031%2Cp_89%3AApple&lo=image&dc&pf_rd_i=13910711&pf_rd_m=A1X6FK5RDHNB96&pf_rd_p=7bfef048-67df-4ecf-bf05-42f49448ccc6&pf_rd_p=7bfef048-67df-4ecf-bf05-42f49448ccc6&pf_rd_r=214Z6SPEBHSAM56PQW8J&pf_rd_r=214Z6SPEBHSAM56PQW8J&pf_rd_s=merchandised-search-leftnav&pf_rd_t=101&qid=1579788647&rnid=1680780031&ref=sr_nr_p_89_1'

# headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}
# source = requests.get(iphones, headers)
# .text

# remove when wze are doing a real scrape

# f = open('source.html', 'w')
# f.write(source.text)
# f.close

with open('source.html') as html_file:
  soup = BeautifulSoup(html_file, 'lxml')

products = soup.find_all(attrs={"data-index": re.compile("^([\s\d]+)$")})

time = str(datetime.datetime.now())

for product in products:
  try:
    title = product.find("span", "a-size-base-plus a-color-base a-text-normal").text
  except AttributeError:
    title = None

  try:
    price = product.find("span", class_="a-price-whole").text
    price = price.replace(",",".")
    price = price.replace("\xa0","")
    price = float(price)
  except AttributeError:
    price = 0

  try:
    slug = "https://www.amazon.fr" + product.find("a", class_="a-link-normal a-text-normal")["href"]
  except AttributeError:
    slug = None

  data = {"title": title, "price": price, "slug": slug, "date": time }
  # uncomment when doing the real shit
  # db.child("amazon").push(data)

# Go through the Data Lake and create a unique collection of amazon products with related id's
amazon_products = db.child("amazon").get()

for saved_product in amazon_products.each():
  saved_product_title = saved_product.val()['title']
  hash_object = hashlib.md5(saved_product_title.encode())
  idKey = hash_object.hexdigest()
  db.child(f"amazon_to_product/{saved_product_title}").set(idKey)

  data = {
    "amazon_url": saved_product.val()['slug'],
    "bm_prices": "",
    "bm_url": "",
    "model": "",
  }
  db.child(f"products/{idKey}").set(data)
  price_collection = { "date": saved_product.val()['date'], "price": saved_product.val()['price'] }
  db.child(f"products/{idKey}/amazon_prices").push(price_collection)

