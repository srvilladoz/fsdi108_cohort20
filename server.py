from flask import Flask, render_template, abort, request
import json
from data import data
from flask_cors import CORS

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
    return json.dumps(data)


@app.route("/api/categories")
def get_categories():
    """
        Get the unique categories from the catalog (data var)
        and return them as a list of string
    """
    return "ok"

if __name__ == '__main__':
    app.run(debug=True)