#!/bin/python3
from bs4 import BeautifulSoup
import json
import requests
import sys


def get_json_content(url):
  page = requests.get(url, headers={"User-Agent": "doesn't matter"})
  soup = BeautifulSoup(page.content, "html.parser")
  script = soup.find(id="__NEXT_DATA__")
  return json.loads(script.contents[0])


def download_song_lyrics(url):
  json_object = get_json_content(url)
  analytics_data = json_object["props"]["pageProps"]["analyticsData"]
  title = f"{analytics_data['lyrics_artist_name']} - {analytics_data['lyrics_name']}"

  data = json_object["props"]["pageProps"]["data"]["trackInfo"]["data"]
  if ("lyrics" in data):
    with open(f"{title}.txt", "w+") as file:
      file.write(data["lyrics"]["body"])
      print(f"Lyrics for {title} downloaded successfully.")
  else:
    print("Lyrics not found for this song.")


if __name__ == "__main__":
  if len(sys.argv) == 1:
    url = input("Song URL: ")
  elif len(sys.argv) == 2:
    url = sys.argv[1]
  else:
    print(
        f'Expected a single argument but received {len(sys.argv)-1}')
    exit()

  download_song_lyrics(url)
