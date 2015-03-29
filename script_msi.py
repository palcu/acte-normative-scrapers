import json
import requests
from bs4 import BeautifulSoup
from pprint import pprint


def get_information(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content)
    return soup.find(class_='content-text').get_text()


def scrape_website(html):
    output = []
    # XXX: Romanian governement FTW
    table_id = 'plcRoot_Layout_zoneMainLeft_pageplaceholder_pageplaceholder_Layout_zoneCenter_pageplaceholder_pageplaceholder_Layout_zoneCenter_ActualizationsArhive_ASPxPageControl1_gvActualizationsByMonth'
    table = BeautifulSoup(html).find(id=table_id)

    titles = table.find_all('h3')
    for index, title in enumerate(titles):
        pretty_url = "http://www.mcsi.ro{0}"
        url_to_article = pretty_url.format(title.find('a').get('href'))

        print("Getting page ({1}/{2}) {0}".format(url_to_article, index+1,
                                                  len(titles)))
        output.append({
            'title': title.get_text().strip(),
            'url': url_to_article,
            'content': [{
                'type': 'text',
                'value': get_information(url_to_article)
            }]
        })
    return output


def main():
    url = 'http://www.mcsi.ro/Minister/Actualizari'
    response = requests.get(url)
    if response.status_code != 200:
        print("Could not get the page {0}".format(url))
        exit(1)
    json_data = json.dumps(scrape_website(response.content), indent=4)
    import ipdb; ipdb.set_trace()
    requests.post('http://localhost:8000/receive_bills/', data=json_data)
    with open('output_msi.json', 'w') as stream:
        stream.write(json_data)


if __name__ == "__main__":
    main()
