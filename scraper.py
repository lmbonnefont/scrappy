from bs4 import BeautifulSoup
import requests
import re

iphones = 'https://www.amazon.fr/s?i=electronics&bbn=218193031&rh=n%3A13921051%2Cn%3A%2113910671%2Cn%3A14060661%2Cn%3A218193031%2Cp_n_operating_system_browse-bin%3A1602846031&lo=image&pf_rd_i=13910711&pf_rd_m=A1X6FK5RDHNB96&pf_rd_p=7bfef048-67df-4ecf-bf05-42f49448ccc6&pf_rd_p=7bfef048-67df-4ecf-bf05-42f49448ccc6&pf_rd_r=214Z6SPEBHSAM56PQW8J&pf_rd_r=214Z6SPEBHSAM56PQW8J&pf_rd_s=merchandised-search-leftnav&pf_rd_t=101&ref=amb_link_30'

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}
source = requests.get(iphones, headers)
#.text

## remove when wze are doing a real scrape
file = open("resp_text.html", "w")
file.write(source.text)
file.close()

f = open('source.html', 'w')
f.write(source.text)
f.close

with open('source.html') as html_file:
  soup = BeautifulSoup(html_file, 'lxml')

# products = soup.find_all(attrs={"data-index": re.compile("^([\s\d]+)$")})

# for product in products:
#   try:
#     title = product.find("span", class_="a-size-base-plus a-color-base a-text-normal").text
#   except AttributeError:
#     title = None

#   try:
#     price = product.find("span", class_="a-offscreen").text
#   except AttributeError:
#     price = None

#   print(f"Title is {title}, price is {price}")
