from bs4 import BeautifulSoup
import requests
import re
import time

username = input("Enter the username: ")
usr_list = [username]

keyword = input("Enter the keyword: ")

file_name = username + "-Magnets.txt"
file = open(file_name, "w")


def parsedPage(Link):
  grabbedPage = requests.get(Link)
  return BeautifulSoup(grabbedPage.content, 'html.parser')


def Parser(storePage):
  for Link in storePage.find_all('a'):
    StrLink = str(Link)
    regexResult = re.search(r'"/(.*)/"', StrLink)
    if regexResult is None:
      continue
    if not 'torrent/' in regexResult.group(1):
      continue
    magnet_link = ("magnet" + re.search(
      r'href="magnet(.*)" onclick',
      str(parsedPage("https://1337x.to/" + regexResult.group(1) +
                     "/"))).group(1)).replace("&amp;", "&")
    if keyword in StrLink:
      print(magnet_link, end="\n\n")
      file.write(magnet_link + "\n\n")


def main(username):
  last_page = int(
    re.search(r'-torrents/(.*)/">Last</a>',
              str(parsedPage("https://1337x.to/" + username +
                             "-torrents/1/"))).group(1))

  start_time = time.time()

  for i in range(1, last_page + 1):
    Parser(
      parsedPage("https://1337x.to/" + username + "-torrents/" + str(i) + "/"))

  elapsed_time = round((time.time() - start_time) / 60, 2)

  print(f"Time Elapsed: {elapsed_time} minutes")

  file.close()


for i in usr_list:
  main(i)
