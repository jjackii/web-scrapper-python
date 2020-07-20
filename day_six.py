import os
import requests
from bs4 import BeautifulSoup
from babel.numbers import format_currency

os.system("clear")

"""
Use the 'format_currency' function to format the output of the conversion
format_currency(AMOUNT, CURRENCY_CODE, locale="ko_KR" (no need to change this one))
"""
url = "https://www.iban.com/currency-codes"

countries = []
exchange = []

request = requests.get(url)
soup = BeautifulSoup(request.text, "html.parser")

table = soup.find("table")
rows = table.find_all("tr")[1:]

for row in rows:
  items = row.find_all("td")
  name = items[0].text
  code =items[2].text
  if name and code:
    country = {
      'name':name.capitalize(),
      'code': code
    }
    countries.append(country)


def final(money):
  country = exchange[0]
  b_country = exchange[1]
  u_url = f"https://transferwise.com/gb/currency-converter/{country['code']}-to-{b_country['code']}"
  convert_request = requests.get(f"{u_url}-rate?amount={money}")
  convert_soup = BeautifulSoup(convert_request.text, "html.parser")
  rate = convert_soup.find("input", {"id":"cc-amount-to"})
  print(rate)
  
  rate = rate['value']
  money = format_currency(money, country['code'], locale="ko_KR")
  rate = format_currency(rate, b_country['code'], locale="ko_KR")
  print(f"{money} is {rate}")


def convert():
  country = exchange[0]
  b_country = exchange[1]
  print(f"How many {country['code']} do you want to convert to {b_country['code']}?")
  try:
    money = int(input())
    final(money)

  except ValueError:
    print("That wasn't a number.")
    convert()

def ask_again():
  print("\nNow choose another country.\n")
  choice_to = int(input("#: "))
  b_country = countries[choice_to]
  print(f"{b_country['name']}\n\n")
  exchange.append(b_country)

def ask():
  try:
    print("\nWhere are you from? Choose a country by number.\n")
    choice = int(input("#: "))
    if choice > len(countries):
      print("Choose a number from the list.")
      ask()
    else:
      country = countries[choice]
      print(f"{country['name']}\n")
      exchange.append(country)

  except ValueError:
    print("That wasn't a number.")
    ask()


print("Welcome to CurrencyConvert PRO 2000")
for index, country in enumerate(countries):
  print(f"#{index} {country['name']}")

ask()
ask_again()
convert()

#error
