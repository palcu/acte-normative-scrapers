import json
import requests
from bs4 import BeautifulSoup


def get_content(url):
    content = []
    response = requests.get(url)
    soup = BeautifulSoup(response.content)
    # Doing this because of the fucking menu
    paragraphs = soup.find(class_='col-content').find_all('p')
    for paragraph in paragraphs:
        for link in paragraph.find_all('a'):
            content.append({
                'value': link.get('href'),
                'type': 'uri'
            })
    return content


def scrape_website(html):
    output = []
    entries = BeautifulSoup(html).find(class_='insiruire').find_all('tr')
    for index, row in enumerate(entries[1:]):
        tds = row.find_all('td')
        url = tds[3].find('a').get('href')
        print("Getting page ({1}/{2}) {0}".format(url, index+1, len(entries)))
        output.append({
            'title': tds[1].get_text().strip(),
            'url': url,
            'content': get_content(url)
        })
    return output


def main():
    url = 'http://www.ancom.org.ro/decizii-ancom_1130'
    response = requests.get(url)
    if response.status_code != 200:
        print("Could not get the page {0}".format(url))
        exit(1)
    json_data = json.dumps(scrape_website(response.content), indent=4)
    requests.post('http://acte-normative.riker.grep.ro/receive_bills', data=json_data)
    with open('output_ancom.json', 'w') as stream:
        stream.write(json_data)


if __name__ == "__main__":
    main()
