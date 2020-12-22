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

@app.route("/keys")
def keys():
    servant_link = []
    servant_key = []
    servant_key.sort()
    url = "https://gamepress.gg/grandorder/servant"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, features="html.parser")
    servant_links = soup.find_all(class_="views-field views-field-title")
    for a in servant_links:
        for i in a.find_all("a"):
            servant_link.append(i.get("href"))
    for key in servant_link:
        servant_key.append(key.split("/")[3])
    return render_template("keys.html", servant_key=sorted(servant_key))


if __name__ == "__main__":
    app.run()