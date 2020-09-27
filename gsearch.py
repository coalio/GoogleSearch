from bs4 import BeautifulSoup as bs
import requests
import json
import re

# Definitions
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
print('Google Search\n')
query = input().replace(' ', '+')
url = f"https://google.com/search?q={query}"

def scrape_links(soup):
  twicks = soup.find_all('div', class_='r')
  anchors = []
  for result in twicks:
      links = result.find_all('a')
      if links:
          link = links[0]['href']
          title = result.find('h3').text
          anchorObject = {
              "title": title,
              "link": link
          }
          anchors.append(anchorObject)
  return anchors

def command(cmd, links):
  if cmd == '':
    print('\nLeaving Google Search')
    exit()
  if cmd == ':q':
    exit()
  else:
    if cmd[0] == '>':
      result = links[int(cmd[1])]
      print('\nFetching: ' + result['title'] + ' (...)')
      response = requests.get(result['link'])
      if response.ok != True:
        print('[' + response.status_code + '] ' + response.text)
      else:
        content = bs(response.content, "html.parser")
        print('[' + result['link'] + ']')
        print(re.sub(r'\n\s*\n', '\n\n', content.get_text()))
    else:
      return search(cmd)

def search(query):
  query = query.replace(' ', '+')
  url = f"https://google.com/search?q={query}"
  response = requests.get(url, headers={"user-agent" : user_agent})
  if response.status_code == 503:
    print('[' + response.url + '] ' + response.text)
    exit()

  results = scrape_links(bs(response.content, "html.parser"))
  
  print('\nShowing results for: ' + query.replace('+', ' '))
  for i in range(len(results)):
    print('['+str(i)+']: ' + results[i]['title'])
  return results

# Get the starting point links

response = requests.get(url, headers={"user-agent" : user_agent})

if response.status_code == 503:
  print('[' + response.url + '] ' + response.text)
  exit()

results = scrape_links(bs(response.content, "html.parser"))

# display the results

print('\nShowing results for: ' + query.replace('+', ' '))
for i in range(len(results)):
  print('['+str(i)+']: ' + results[i]['title'])

currPage = results
while True:
  print('\n>> ', end='', flush=True)
  update = command(input(), currPage)
  if update:
    currPage = update