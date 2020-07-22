import requests
from flask import Flask, render_template, request

base_url = "http://hn.algolia.com/api/v1"

# This URL gets the newest stories.
new = f"{base_url}/search_by_date?tags=story"

# This URL gets the most popular stories
popular = f"{base_url}/search?tags=story"

# popular = requests.get(popular).json()["hits"]
# new = requests.get(new).json()["hits"]


# for popular in popular:
#   home = {
#     "title" : popular["title"],
#     "link" : popular["url"],
#     "point" : popular["points"],
#     "author" : popular["author"],
#     "comments" : popular["num_comments"]
#   }
#   po_id = popular["objectID"]
#   print(home)




# This function makes the URL to get the detail of a storie by id.
# Heres the documentation: https://hn.algolia.com/api
def make_detail_url(id):
  return f"{base_url}/items/{id}"

db = {}
app = Flask("DayNine")

@app.route("/")
def home():
  order_by = request.args.get("order_by", "popular")
  if order_by not in db:
    if order_by == "popular":
      url = requests.get(popular).json()["hits"]
    elif order_by == "new":
      url = requests.get(new).json()["hits"]
    db[order_by] = url
  url = db[order_by]  
  return render_template("index.html", order_by=order_by, url=url)

@app.route("/<id>")
def detail(id):
  url = make_detail_url(id)
  url_id = requests.get(url).json()
  return render_template("detail.html", url_id=url_id)

app.run(host="0.0.0.0")
