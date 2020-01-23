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
  saved_product_title = amazon_product.val()['title']
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
          "price": amazon_product.val()['price']}
  return price



