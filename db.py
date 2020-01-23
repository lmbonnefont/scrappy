import pyrebase

## to be changed with the new db of antoine
config = {
  "apiKey": "AIzaSyCfLzXJ2domxHJxXS4qrBXG3m0G1KQVL38",
  "authDomain": "windmill-fc2d9.firebaseapp.com",
  "databaseURL": "https://windmill-fc2d9.firebaseio.com",
  "storageBucket": "windmill-fc2d9.appspot.com"
}

firebase = pyrebase.initialize_app(config)

# Get a reference to the auth service
auth = firebase.auth()

# Log the user in
user = auth.sign_in_with_email_and_password(email, password)

# Get a reference to the database service
db = firebase.database()

data = {"title": "Apple Ipad", "price": "290€"}
db.child("amazon_products").push(data)

products = db.child("amazon_products").get()
for product in products.each():
    print(product.val())

