import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request, url_for, redirect
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        svt = request.form["nm"]
        return redirect(url_for("image_get", servant=svt))
    else:
        return render_template("index.html")

@app.route("/processing/<servant>/")
def image_get(servant):
    src_list = []
    count = 0
    desktop = os.environ['USERPROFILE'] + "\Desktop\\" + str(servant).capitalize() + "\\"
    os.mkdir(desktop)
    servant_url = "https://gamepress.gg/grandorder/servant/" + servant
    r = requests.get(servant_url)
    soup = BeautifulSoup(r.text, features="html.parser")
    images = soup.find_all(class_="image-style-servant-image")
    for img in images:
        src = img.get("src")
        if src:
            src_list.append(src)
    for link in src_list:
        count += 1
        image_url = "http://gamepress.gg" + link
        r2 = requests.get(image_url)
        with open(desktop.replace("\\", "/") + str(servant) + str(count) + ".png", "wb") as f:
            f.write(r2.content)
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run()