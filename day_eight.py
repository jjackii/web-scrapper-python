import os
import csv
import requests
from bs4 import BeautifulSoup

os.system("clear")
alba_url = "http://www.alba.co.kr"

def scrap(job):
  file = open(f"{job['company']}.csv", mode="w")
  writer = csv.writer(file)
  writer.writerow(["place", "title", "time", "pay", "date"])
  for i in job["job_data"]:
    writer.writerow(list(i.values()))


request = requests.get(alba_url)
soup = BeautifulSoup(request.text, "html.parser")
brands = soup.find_all("li", {"class": "impact"})
for brand in brands:
  brand = brand.find("a")
  link = brand["href"]
  company = brand.find_all("span")[1].string
  job = {
    "company": company,
    "job_data": []
  }
  jobs_request = requests.get(link)
  jobs_soup = BeautifulSoup(jobs_request.text, "html.parser")
  tbody = jobs_soup.find("div", {"id": "NormalInfo"}).find("tbody")
  rows = tbody.find_all("tr", {"class":""})
  for row in rows:
    place = row.find("td", {"class": "local"})
    if place:
      place = place.text
    title = row.find("td", {"class": "title"})
    if title:
      title = title.find("span").string  
    time = row.find("td", {"class": "data"})
    if time:
      time = time.find("span").string
    pay = row.find("td", {"class": "pay"})
    if pay:
      pay = pay.text
    date = row.find("td", {"class": "regDate"})
    if date:
      date = date.text 
    data = {
      "place": place,
      "title": title,
      "time": time,
      "pay": pay,
      "date": date
    }
    job["job_data"].append(data)
  scrap(job)
