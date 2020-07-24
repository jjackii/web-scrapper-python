import requests
from flask import Flask, render_template, request
from bs4 import BeautifulSoup

"""
When you try to scrape reddit make sure to send the 'headers' on your request.
Reddit blocks scrappers so we have to include these headers to make reddit think
that we are a normal computer and not a python script.
How to use: requests.get(url, headers=headers)
"""

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}


"""
All subreddits have the same url:
i.e : https://reddit.com/r/javascript
You can add more subreddits to the list, just make sure they exist.
To make a request, use this url:
https://www.reddit.com/r/{subreddit}/top/?t=month
This will give you the top posts in per month.
"""

subreddits = [
    "javascript",
    "reactjs",
    "reactnative",
    "programming",
    "css",
    "golang",
    "flutter",
    "rust",
    "django"
]


app = Flask("DayEleven")

URL = "https://www.reddit.com"

@app.route("/")
def home():
  return render_template("home.html")

@app.route("/read")
def read():
  subreddits = list(request.args.keys())
  records = []
  if subreddits:
    for subreddit in subreddits:
      url = f"{URL}/r/{subreddit}/top/?t=month"
      url = requests.get(url, headers=headers)
      soup = BeautifulSoup(url.text, "html.parser")
      results = soup.find_all("div", {"class": "_1oQyIsiPHYt6nx7VOmd1sz"})      
      for result in results:
        vote = result.find("div", {"class": "_1rZYMD_4xY3gRcSS3p8ODO"}).string
        news = result.find("div", {"class": "y8HYJ-y_lTUHkQIc1mdCq"})
        title = news.find("h3").string
        link = news.find("a")["href"]
        link = f"{URL}{link}"
        if "k" not in vote:
          if "https://alb" not in link:
            record = (
              int(vote),
              title,
              link,
              subreddit
            )
            if record not in records:
              records.append(record)
  records.sort(reverse=True)     
  print(records)
  return render_template("read.html", subreddits=subreddits, records=records)

app.run(host="0.0.0.0")
