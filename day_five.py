import os
import requests
from bs4 import BeautifulSoup

os.system("clear")
url = "https://www.iban.com/currency-codes"

currency_codes = []

get_page = requests.get(url)
soup = BeautifulSoup(get_page.text, "html.parser")
extract_page = soup.select("tbody > tr")

for item in extract_page:
  item = item.find_all("td")
  country = item[0].text
  code = item[2].text
  if code != "":
    obj = {
      "country": country.capitalize(),
      "code": code
    }
    currency_codes.append(obj)

def user_input():
  try:
    user = int(input("#: "))
    if user > len(currency_codes):
      print("Choose a number from the list.")
      user_input()
    else:
      name = currency_codes[user]  
      print(f"You chose {name['country']}\nThe currency code is {name['code']}")
  except ValueError:
    print("That wasn't a number.")
    user_input()    

print("Hello! Please choose select a country by number:")
for num, name in enumerate(currency_codes):
  print(f"# {num} {name['country']}")

user_input()  
