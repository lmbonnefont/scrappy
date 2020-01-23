from bs4 import BeautifulSoup
import requests
import re
import pyrebase
import json
import matcher
import data_builder

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

#Building the amazon data
arr_amazon_products = data_builder.data_for_amazon(products)

# uncomment when doing the real shit to push the data to the amazon table
# for amazon_product in arr_amazon_products:
#   db.child("amazon").push(amazon_product)


# Go through the Data Lake and create a unique collection of amazon products with related id's. Push to Algolia_to_product table
amazon_products = db.child("amazon").get()
for amazon_product in amazon_products.each():
  saved_product_title, idKey = data_builder.data_for_amazon_to_product(amazon_product)
  db.child(f"amazon_to_product/{saved_product_title}").set(idKey)

  #Push the data to the clean product table
  data = data_builder.data_clean_product(amazon_product)
  db.child(f"products/{idKey}").set(data)

  #Push the price inside the price collection of the clean products
  price_collection = data_builder.price_collection_amazon(amazon_product)
  db.child(f"products/{idKey}/amazon_prices").push(price_collection)

