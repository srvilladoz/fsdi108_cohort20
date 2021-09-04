from flask import Flask, render_template, abort, request
import json
from pymongo import cursor, results
from data import data
from flask_cors import CORS
from config import db, parse_json

app = Flask(__name__) # create a flask app
CORS(app)

me = {
    "name": "Sarah",
    "last_name": "Villadoz",
    "age": 29,
    "email": "srvilladoz@gmail.com",
    "address": {
        "street": "Answer to life",
        "number": 42
    }
}


@app.route('/')
@app.route('/home')
def home_page():
    return render_template("index.html")


@app.route("/about")
def about_me():
    return me["name"] + " " + me["last_name"]

# /about/email
@app.route("/about/email")
def about_me_email():
    return me["email"]


@app.route("/api/catalog")
def get_catalog():
    cursor = db.products.find({})
    prods = [ prod["title"] for prod in cursor ]
    
    return parse_json(prods)

@app.route("/api/catalog", method=['POST'])
def save_product():
    product = request.get_json() #return a dict

    #validations
    if not "title" in product:
        return parse_json({"Error": "title is required", "success": False})

    if not "price" in product or not product["price"]:
        return parse_json({"Error": "price is required and cannot be free", "success": False})


    db.products.insert_one(product)

    return parse_json(data)

@app.route("/api/couponCodes/<code>")
def get_coupon(code):
    code = db.couponCodes.find_one({"code": code})
    return parse_json(code)

@app.route("/api/couponCodes")
def get_coupons():
    cursor = db.couponCodes.find({})
    codes = [code for code in cursor]
    return parse_json(codes)


@app.route("/api/couponCodes", methods=["POST"])
def save_coupon():
    coupon = request.get_json()

    #validations
    if not "code" in coupon:
        return parse_json({"error" : "code is required", "success": False})

    if not "discount" in coupon or not coupon ["discount"]:
        return parse_json({"error": "discount is required, and should not be zero", "success": False})

    db.couponCodes.insert_one(coupon)
    return parse_json(coupon)


@app.route("/api/categories")
def get_categories():
    """
        Get the unique categories from the catalog (data var)
        and return them as a list of string
    """
    cursor = db.products.find({})
    categories = []
    for item in cursor:
        cat = item["category"]

        if cat not in categories:
            categories.append(cat)

    return parse_json(categories)

@app.route("/api/catalog/id/<id>")
def get_product_by_id(id):
    product = db.products.find_one({"_id": id})
    if not product:
        abort(404)

    return parse_json(product)
   

    for item in data:
        if(str(item["_id"]) == id):
            return parse_json(item)

    abort(404)


@app.route("/api/catalog/category/<category>")
def get_products_by_category(category):
    cursor = db.products.find({ "category": category })
    results = [prod for prod in cursor]
    return parse_json(results)

#/api/catalog/cheapest
# get the cheapest product on the catalog
@app.route("/api/catalog/cheapest")
def get_cheapest():
    cheapest = data[0]
    for item in data:
        if(item["price"] < cheapest["price"]):
            cheapest = item

    return parse_json(cheapest)

@app.route("api/test/populatedb")
def populate_db():
    for prod in data:
        db.products.insert_one(prod)

    return "Data loaded"


########## Orders Login ##########
@app.route("/api/orders", methods=["post"])
def save_order():
    order = request.get_json()

    #validate at least 1 product
    prods = order["products"]
    count = len(prods)
    if(count < 1)
        # 400 bad request (blaming the client)
        abort(400, "Error: Orders without products are not allowed!")

    #get the prices for the items included
    total = 0
    for item in prods: 
        id = item["_id"]
        print(id)

        db_item = db.products.find_one({"_id": id})
        item["price"] = db_item["price"]
        total += db_item["price"]
        print(db_item["price"])

    #calculate the order total
    #order["total"] = x

    print("The total is: ", total)
    order["total"] = total

    #verify and apply couponCode
    if "couponCode" in order and order["couponCode"]:
        #validate
        code = order ["couponCode"]
        coupon = db.couponCodes.find_one({"code": code})
        if coupon:
            discount = coupon["discount"]
            total = total - (total * discount) / 100
            order["total"] = total
        else:
            order["couponCode"] = "INVALID"

    db.orders.insert_one(order)
    return parse_json(order)

@app.route("/api/orders")
def get_orders():
    cursor = db.orders.find({})
    orders = [order for order in cursor]
    return parse_json(orders)


@app.route( "/api/orders", methods =["post"])
def save_order():
    order = request.get_json()
    
#validate at least 1 product
    prods = order["products"]
    count = len(prods)
    if(count < 1):
        #400 bad request (blaming the client)
        abort(400, "Error: Orders without product")


    db.orders.insert_one(order)
    return parse_json(order)

@app.route("/api/orders")
def get_orders():
    cursor = db.orders.find({})
    order = [order for order in cursor]
    return parse_json(order)

@app.route("/api/orders/<userId>")
def get_order_for_user(userId):
    cursor = db.orders.find({"userId": userId})
    orders = [order for order in cursor]
    return parse_json(orders)



if __name__ == '__main__':
    app.run(debug=True)


# coupon codes
# db.couponCodes
# code, discount

# create a GET to real all
# create a POST to add
# create a GET to search by code
