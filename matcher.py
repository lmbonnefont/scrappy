import json

with open('algolia.json') as f:
    d = json.load(f)

print (type(d))
algolia_products = d["results"][0]["hits"]

for item in algolia_products:
  
# print(d['results'])