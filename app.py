from flask import Flask, render_template, request
import requests
import json
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://{}:{}@{}:{}/{}]".format(
    os.getenv("DB_USER"),
    os.getenv("DB_PASSWORD"),
    os.getenv("DB_HOST"),
    os.getenv("DB_PORT"),
    os.getenv("DB_NAME"),
)
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return "<User %r>" % self.username


url = "https://covid-193.p.rapidapi.com/statistics"

headers = {
    "X-RapidAPI-Host": "covid-193.p.rapidapi.com",
    "X-RapidAPI-Key": "ad653f0046mshbbe0b5e5f115b95p1fe7d4jsne395e329b0e7",
}


@app.route("/", methods=["GET"])
def index():
    req = requests.get(url, headers=headers)
    data = json.loads(req.content)

    return render_template("index.html", data=data, url=url)


@app.route("/sonuc", methods=["GET", "POST"])
def sonuc():
    select = request.form.get("comp_select")

    req = requests.get(url, headers=headers)
    data = json.loads(req.content)

    country_name = ""
    deaths_number = ""
    day = ""
    newOlum = ""
    toplamOlum = ""
    casesJSON = ""
    yeniVaka = ""
    toplamVaka = ""
    for row in data["response"]:
        if select == row["country"]:
            country_name = select
            deaths_number = row["deaths"]
            newOlum = deaths_number["new"]
            toplamOlum = deaths_number["total"]
            day = row["day"]
            casesJSON = row["cases"]
            yeniVaka = casesJSON["new"]
            toplamVaka = casesJSON["total"]

    return render_template(
        "result.html",
        country_name=country_name,
        deaths_number=deaths_number,
        day=day,
        newOlum=newOlum,
        toplamOlum=toplamOlum,
        casesJSON=casesJSON,
        toplamVaka=toplamVaka,
        yeniVaka=yeniVaka,
    )


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000)
