# BEGIN CODE HERE
from flask import Flask, request
from flask_pymongo import PyMongo
from flask_cors import CORS
from pymongo import TEXT
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
    return ""
    # END CODE HERE
