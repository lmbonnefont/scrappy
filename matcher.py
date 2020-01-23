from difflib import SequenceMatcher

def normaliseString(a):
  a = a.replace("(", "")
  a = a.replace(")", "")
  a = a.replace("\xa0","")
  a = a.replace("-", "")
  a = a.replace("Débloqué", "")
  a = a.replace("Apple", "")
  a = a.replace("débloqué", "")
  a = a.replace("apple", "")
  return a

algoliaTitle = normaliseString(a)
amazonTitle = normaliseString(b)
ratio = SequenceMatcher(None, a, b).ratio()

print(ratio)