# BEGIN CODE HERE
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS
from pymongo import TEXT

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

options = Options()
options.headless = True
driver = webdriver.Chrome(options=options)
driver.get("https://qa.auth.gr/el/x/studyguide/600000438/current")

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
    return ""
    # END CODE HERE


@app.route("/crawler", methods=["GET"])
def crawler():
    # BEGIN CODE HERE
    try:
        semester = request.args.get("semester")
        xpath = f"//*[@id='exam{semester}']/tbody/tr"
        elements = driver.find_elements(By.XPATH, xpath)
        course_titles = [_.get_attribute('coursetitle') for _ in elements]

        if len(course_titles ) == 0:
            return "BAD REQUEST", 400
        return jsonify(course_titles), 200

    except Exception as e:
        return "BAD REQUEST", 400
    # END CODE HERE
