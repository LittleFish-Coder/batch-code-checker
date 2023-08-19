from selenium import webdriver
from website1 import check_from_cosmetic_momoko
from website2 import check_from_check_fresh
from website3 import check_from_cosmetic_calculator
from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import time

app = Flask(__name__, static_folder="static")


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/result", methods=["POST"])
def calculate():
    uploaded_file = request.files["file"]
    if uploaded_file:
        # Process the file (e.g., read Excel, perform calculations)
        # df = pd.read_excel(uploaded_file)
        result = "File processed successfully."
    else:
        result = "No file uploaded."

    return result  # Return the result to be displayed on the webpage


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
