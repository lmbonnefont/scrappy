from difflib import SequenceMatcher

def normaliseString(a):
  a = a.replace("(", "")
  a = a.replace(")", "")
  a = a.replace("\xa0","")
  a = a.replace(" - ", "")
  a = a.replace("-", "")
  a = a.replace("  "," ")
  a = a.replace("Débloqué", "")
  a = a.replace("Apple ", "")
  a = a.replace("débloqué ", "")
  a = a.replace("apple ", "")
  a = a.replace("Reconditionné", "")
  a = a.replace("reconditionné", "")
  a = a.strip()
  return a

def normaliseNumber(num):
  num = num.replace(",",".")
  num = num.replace("\xa0","")
  return num


def similarity(algolia, amazon):
  return SequenceMatcher(None, algolia, amazon).ratio()
