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
    return ""
    # END CODE HERE


@app.route("/add-product", methods=["POST"])
def add_product():
    # BEGIN CODE HERE
    return ""
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
