from bs4 import BeautifulSoup
import requests
import re
import pyrebase
import json
import matcher
import data_builder
import datetime

pyrebase_config = {
  "apiKey": "AIzaSyCKh0Rg_sQuFH83Ev4eTZ4TxLYYQ2ui59w",
  "authDomain": "scrappy-896fd.firebaseapp.com",
  "databaseURL": "https://scrappy-896fd.firebaseio.com",
  "storageBucket": "scrappy-896fd.appspot.com"
}

firebase = pyrebase.initialize_app(pyrebase_config)

# Get a reference to the database service
db = firebase.database()

urlSources = [
 'https://www.amazon.fr/s?i=electronics&bbn=218193031&rh=n%3A13921051%2Cn%3A13910671%2Cn%3A14060661%2Cn%3A218193031%2Cp_89%3AApple&lo=image&dc&pf_rd_i=13910711&pf_rd_m=A1X6FK5RDHNB96&pf_rd_p=7bfef048-67df-4ecf-bf05-42f49448ccc6&pf_rd_p=7bfef048-67df-4ecf-bf05-42f49448ccc6&pf_rd_r=214Z6SPEBHSAM56PQW8J&pf_rd_r=214Z6SPEBHSAM56PQW8J&pf_rd_s=merchandised-search-leftnav&pf_rd_t=101&qid=1579788647&rnid=1680780031&ref=sr_nr_p_89_1',
 'https://www.amazon.fr/s?i=electronics&bbn=218193031&rh=n%3A13921051%2Cn%3A13910671%2Cn%3A14060661%2Cn%3A218193031%2Cp_89%3AApple&lo=image&dc&page=2&pf_rd_i=13910711&pf_rd_m=A1X6FK5RDHNB96&pf_rd_p=7bfef048-67df-4ecf-bf05-42f49448ccc6&pf_rd_p=7bfef048-67df-4ecf-bf05-42f49448ccc6&pf_rd_r=214Z6SPEBHSAM56PQW8J&pf_rd_r=214Z6SPEBHSAM56PQW8J&pf_rd_s=merchandised-search-leftnav&pf_rd_t=101&qid=1579860492&rnid=1680780031&ref=sr_pg_2',
 'https://www.amazon.fr/s?i=electronics&bbn=218193031&rh=n%3A13921051%2Cn%3A13910671%2Cn%3A14060661%2Cn%3A218193031%2Cp_89%3AApple&lo=image&dc&page=3&pf_rd_i=13910711&pf_rd_m=A1X6FK5RDHNB96&pf_rd_p=7bfef048-67df-4ecf-bf05-42f49448ccc6&pf_rd_p=7bfef048-67df-4ecf-bf05-42f49448ccc6&pf_rd_r=214Z6SPEBHSAM56PQW8J&pf_rd_r=214Z6SPEBHSAM56PQW8J&pf_rd_s=merchandised-search-leftnav&pf_rd_t=101&qid=1579860500&rnid=1680780031&ref=sr_pg_3',
 'https://www.amazon.fr/s?i=electronics&bbn=218193031&rh=n%3A13921051%2Cn%3A13910671%2Cn%3A14060661%2Cn%3A218193031%2Cp_89%3AApple&lo=image&dc&page=4&pf_rd_i=13910711&pf_rd_m=A1X6FK5RDHNB96&pf_rd_p=7bfef048-67df-4ecf-bf05-42f49448ccc6&pf_rd_p=7bfef048-67df-4ecf-bf05-42f49448ccc6&pf_rd_r=214Z6SPEBHSAM56PQW8J&pf_rd_r=214Z6SPEBHSAM56PQW8J&pf_rd_s=merchandised-search-leftnav&pf_rd_t=101&qid=1579860526&rnid=1680780031&ref=sr_pg_4',
 'https://www.amazon.fr/s?i=electronics&bbn=218193031&rh=n%3A13921051%2Cn%3A13910671%2Cn%3A14060661%2Cn%3A218193031%2Cp_89%3AApple&lo=image&dc&page=5&pf_rd_i=13910711&pf_rd_m=A1X6FK5RDHNB96&pf_rd_p=7bfef048-67df-4ecf-bf05-42f49448ccc6&pf_rd_p=7bfef048-67df-4ecf-bf05-42f49448ccc6&pf_rd_r=214Z6SPEBHSAM56PQW8J&pf_rd_r=214Z6SPEBHSAM56PQW8J&pf_rd_s=merchandised-search-leftnav&pf_rd_t=101&qid=1579860547&rnid=1680780031&ref=sr_pg_5',
]

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}

products = []
for urlSource in urlSources:
  rawHtml = requests.get(urlSource, headers).text

  soup = BeautifulSoup(rawHtml, 'lxml')


  productsCollection = soup.find_all(attrs={"data-index": re.compile("^([\s\d]+)$")})
  products = products + productsCollection

# #Building the amazon data
arr_amazon_products = data_builder.data_for_amazon(products)

print(len(arr_amazon_products))

#uncomment when doing the real shit to push the data to the amazon table
for amazon_product in arr_amazon_products:
  db.child("amazon").push(amazon_product)


#Go through the Data Lake and create a unique collection of amazon products with related id's. Push to Algolia_to_product table
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



#Getting the Algolia results from the json
with open('algolia_saved.json', 'r') as f:
  payload_algolia = json.load(f)

#Isolate the algolia product info into a dict ("title", "algolia_clean_title", "algolia_price", "bm_url", "date")
data_algolia = data_builder.data_for_algolia(payload_algolia)

#Getting the keys and clean title of Amazon
amazon_products = db.child("amazon_to_product").get()

#Creating a dict with Amazon products{clean_title: id matching}
dict_amazon_products = {}
for amazon_product in amazon_products.each():
  dict_amazon_products[amazon_product.key()] = amazon_product.val()

#As we got listings info from Algolia, several listings title will match an Amazon product.
#prices_matched_id is a dict storing the ids and the price of the already matched product.
#We will only keep in this dict the most expansive BM listing to be compared to Amazon product.
prices_matched_id = {}
for elt_algolia in data_algolia:

  found_match = False

  for title_amazon in dict_amazon_products:
    score = matcher.similarity(elt_algolia["algolia_clean_title"], title_amazon)
    #This threesold is based on observation. You can play with it. If you lower it to 0.92 the matches are not good.
    if score > 0.94:
      #We say that we found a match to no push a new product
      found_match = True
      #If the id is not in the already matched id we add it to the dict
      if dict_amazon_products[title_amazon] not in prices_matched_id:
        prices_matched_id[dict_amazon_products[title_amazon]] = elt_algolia["algolia_price"]
      #If the id is found in the dict, we check if the listing is more expansive than the one we already matched.
      # We replace it in the dict if so.
      else:
        data_builder.is_listing_more_expansive(prices_matched_id, elt_algolia, dict_amazon_products[title_amazon])
      #We update the bm url. This is crade but it's late right now.
      db.child(f"products/{dict_amazon_products[title_amazon]}").update({"bm_url": elt_algolia["bm_url"]})

      break

  if not found_match:
    #Pushing clean Algolia products to product table
    data, idKey = data_builder.data_clean_product_algolia(elt_algolia)
    db.child(f"products/{idKey}").set(data)
    #Pushing prices to Algolia prices
    db.child(f"products/{idKey}/bm_prices").push({"date": str(datetime.datetime.now()), "value": elt_algolia["algolia_price"]})

#We push the prices BM corresponding to the most expansive listings
print(f"Il y a {len(prices_matched_id)} matchs")
print("Les ids matchés sont:")
for match in prices_matched_id:
  #ids of the products matched
  print(match)
  db.child(f"products/{match}/bm_prices").push({"date": str(datetime.datetime.now()), "value": prices_matched_id[match]})






