import os
import requests

def restart():
  print("Do you want to start over? y/n")
  check = input()
  if check is "y" or "n":
    if check is "y":
      start()
    else:
      print("k. bye!")
  else:
    print("That's not a valid answer")
    restart()  

def start():
  os.system("clear")
  print("Welcome to IsItDown.py!", "\nPlease write a URL or URLs you want to check. (separated by comma)")
  urls = str(input()).lower().split(",")
  for url in urls:
    url = url.strip()
    if ".com" in url:
      if "http://" not in url:
        url = f"http://{url}"
      try:
        r = requests.get(url)
        if r.status_code == 200:
          print(url, "is up!")
        else:
          print(url, "is down!")
      except:
        print(url, "is down!")      
    else:
      print(f"{url} is not a valid URL. ") 
  restart()     

start()
