# web scraper to get contact info from a phone book in Switzerland
# Author: Per Idar Rød
# Creation date: 15.02.2023
# Contact me on email: post@peridar.net

import requests
from bs4 import BeautifulSoup
import csv


# load the page
def getdata(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; U; Android 4.2.2; he-il;\
                NEO-X5-116A Build/JDQ39) AppleWebKit/534.30\
                (""KHTML, like Gecko) Version/4.0 Safari/534.30"}
    r = requests.get(url, headers=headers)
    webpage = r.content
    soup = BeautifulSoup(webpage, "html.parser")
    # print(soup)
    return soup


# function to find next url to go to
def getnextpage(soup):
    if soup:
        page = soup.find('ul', {'class': 'pagination'})
        if page.find('a', {'rel': 'next'}):
            url = 'https://www.local.ch' + \
                str(page.find('a', {'rel': 'next'})['href'])
            return url
        else:
            return


# data extraction
def extract_info(soup):
    cards = soup.find_all('div', 'entry-card')
    page_cards = []
    for card in cards:
        # find name
        name = card.find('h2').text.strip()

        # find address
        address = card.find('div', 'card-info-address').find('span')

        # find phone number
        try:
            tel = card.find('a', {'title': 'Call'})['href'].split(':')[1]
        except TypeError as err:
            tel = None
        # find email address
        try:
            mail = card.find('a', {'title': 'E-Mail'})['href'].split(':')[1]
        except TypeError as err:
            mail = None

        # save the data in a dict
        card = {
            'Name': name,
            'Address': address.string,
            'Phone Number': tel,
            'E-mail': mail,
        }
        page_cards.append(card)

    return page_cards


# function to save data to csv file
def save_csv(results):

    keys = results[0].keys()

    with open('contact_info.csv', 'w', newline='', encoding='utf-8') as f:
        dict_writer = csv.DictWriter(f, keys,)
        dict_writer.writeheader()
        dict_writer.writerows(results)


# main function to run all of this
def main():

    url = 'https://www.local.ch/en/q?what\
            =clinique&where=Switzerland&rid=iL-4&slot=tel'

    results = []
    while True:
        soup = getdata(url)
        results.extend(extract_info(soup))
        url = getnextpage(soup)
        print(url)
        if not url:
            break

    save_csv(results)


# all good? run main function from this file
if __name__ == '__main__':
    main()
