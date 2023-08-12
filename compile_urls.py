# ------------
# program for compiling a list of provider homepage urls from healthgrades.com
# list of urls exported to data/urls.csv
# ------------

import requests
from bs4 import BeautifulSoup
from gzip import decompress
import pandas as pd

# load sitemap
url = "https://www.healthgrades.com/sitemapindex.xml"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"}
content = requests.get(url, headers=headers, stream=True)
soup = BeautifulSoup(content.text, features="xml")

# find all profile links
links = soup.find_all("loc")
files = []
for link in links:
    if link.text.find("profile") == -1:
        continue
    files.append(link.text)

# helper variables to track extraction progress
length = len(files)
count = 0

# unzip profiles links and extract doctor urls
doctors = []
for file in files:
    r = requests.get(file, stream=True)
    soup = BeautifulSoup(decompress(r.content), features="xml")
    urls = soup.find_all("loc")
    for url in urls:
        doctors.append(url.text)
    count += 1
    print(str(count) + " specialities added out of " + str(length))

# process doctor urls and export to urls.csv
df = pd.DataFrame({'url': doctors})
df.drop_duplicates(subset=None, keep="first", inplace=True)
print(df.describe())
df.to_csv('data/urls.csv', header=False, index=False, encoding='utf-8')
