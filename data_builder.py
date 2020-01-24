import matcher
import datetime
import hashlib

def data_for_amazon(products):
  arr_data = []
  time = str(datetime.datetime.now())

  for product in products:
    try:
      title = product.find("span", "a-size-base-plus a-color-base a-text-normal").text
    except AttributeError:
      title = None

    try:
      price = product.find("span", class_="a-price-whole").text
      price = matcher.normaliseNumber(price)
      price = float(price)
    except AttributeError:
      price = 0

    try:
      slug = "https://www.amazon.fr" + product.find("a", class_="a-link-normal a-text-normal")["href"]
    except AttributeError:
      slug = None

    title_clean = matcher.normaliseString(title)


    data = {"title": title, "price": price, "slug": slug, "date": time, "title_clean": title_clean }
    arr_data.append(data)
  return arr_data


def data_for_amazon_to_product(amazon_product):
    #creation of the title
  saved_product_title = amazon_product.val()['title_clean']
  # creation of the id
  hash_object = hashlib.md5(saved_product_title.encode())
  idKey = hash_object.hexdigest()
  return(saved_product_title,idKey)


def data_clean_product(amazon_product):
  data = {
    "amazon_url": amazon_product.val()['slug'],
    "bm_prices": "",
    "bm_url": "",
    "model": amazon_product.val()['title'],
  }
  return data

def price_collection_amazon(amazon_product):
  price = {"date": amazon_product.val()['date'],
          "value": amazon_product.val()['price']}
  return price

def price_collection_algolia(algolia_product):
  price = {"date": algolia_product["date"],
           "value": algolia_product["algolia_price"]
  }
  return price

def data_for_algolia(dict):
  time = str(datetime.datetime.now())
  results = []
  number_of_results = len(dict["results"][0]["hits"])
  for i in range(0,number_of_results):
    algolia_title = dict["results"][0]["hits"][i]["title"]
    algolia_clean_title = matcher.normaliseString(algolia_title)
    algolia_price = dict["results"][0]["hits"][i]["price"]
    bm_url = "https://www.backmarket.fr/" + dict["results"][0]["hits"][i]["slug"]
    data_algolia = {"title":algolia_title, "algolia_clean_title":algolia_clean_title, "algolia_price": algolia_price, "bm_url": bm_url, "date": time}
    results.append(data_algolia)
  return results

def is_listing_more_expansive(dict_matched_id, elt_algolia, key_matched_id):
  if dict_matched_id[key_matched_id] < elt_algolia["algolia_price"]:
    dict_matched_id[key_matched_id] = elt_algolia["algolia_price"]
  return dict_matched_id









