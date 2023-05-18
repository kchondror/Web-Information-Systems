# BEGIN CODE HERE
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS
from pymongo import TEXT

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

options = Options()
options.headless = True
driver = webdriver.Chrome(options=options)
driver.get("https://qa.auth.gr/el/x/studyguide/600000438/current")

import numpy as np
from numpy.linalg import norm
# END CODE HERE

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://127.0.0.1:27017/pspi"
CORS(app)
mongo = PyMongo(app)
mongo.db.products.create_index([("name", TEXT)])


@app.route("/search", methods=["GET"])
def search():
    # BEGIN CODE HERE

    name = request.args.get("name")
    if not name:
        return {"error": "Missing name parameter"}, 400
    filtered_products = mongo.db.products.find({"name": {"$regex": fr"\b{name}\b", "$options": "i"}}).sort("price", -1)
    # This implementation of fuzzy searching is doing implemented using regular expressions,
    # We check for whole words matches

    products = []
    for product in filtered_products:
        product["_id"] = str(product.pop("_id"))
        products.append(product)

    return products
    # END CODE HERE


@app.route("/add-product", methods=["POST"])
def add_product():
    # BEGIN CODE HERE

    new_product: dict = request.json
    # Check if JSON body is valid
    keys = {'name', 'production_year', 'price', 'color', 'size'}
    if not (set(new_product.keys()) == keys):
        extra_fields = set(new_product.keys()) - keys
        missing_fields = keys - set(new_product.keys())
        error_message: str = "Error with JSON body:{0}{1}".format(
            (f"has extra body parameters {extra_fields},   " if extra_fields else ""),
            (f"has missing body parameters {missing_fields}" if missing_fields else ""))
        return {'error': error_message}, 400

    db_result = mongo.db.products.update_one({'name': new_product['name']},
                                             {"$set": {
                                                 'production_year': new_product['production_year'],
                                                 'price': new_product['price'],
                                                 'color': new_product['color'],
                                                 'size': new_product['size']
                                             }
                                             }, upsert=True)
    # upsert
    # Creates a new document if no documents match the filter.
    # Updates a single document that matches the filter.

    if db_result.upserted_id is not None:
        return "Inserted"
    else:
        return "Updated"

    # END CODE HERE


@app.route("/content-based-filtering", methods=["POST"])
def content_based_filtering():
    # BEGIN CODE HERE
    productsArray = []

    current_product = request.json
    current_product = np.array([current_product["production_year"],
                                current_product["price"],
                                current_product["color"],
                                current_product["size"]])

    Qresult = list(mongo.db.products.find({}))
    for document in Qresult:
        product = np.array([document["production_year"],
                            document["price"],
                            document["color"],
                            document["size"]])

        cosine = np.dot(current_product, product) / (norm(current_product) * norm(product)) * 100
        if cosine > 70:
            productsArray.append(document["name"])

    return productsArray
    # END CODE HERE


@app.route("/crawler", methods=["GET"])
def crawler():
    # BEGIN CODE HERE
    try:
        semester: str | None = request.args.get("semester")
        xpath: str = f"//*[@id='exam{semester}']/tbody/tr"
        elements: list[WebElement] = driver.find_elements(By.XPATH, xpath)
        course_titles: list[str] = [_.get_attribute('coursetitle') for _ in elements]

        if len(course_titles) == 0:
            return "BAD REQUEST", 400
        return jsonify(course_titles), 200

    except Exception as e:
        return "BAD REQUEST", 400
    # END CODE HERE
