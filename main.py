import click
import pandas as pd
import requests as http
from bs4 import BeautifulSoup
from _datetime import datetime


@click.group()
def run():
    pass


@run.command(help='A command to get data from myhome.ge')
def myhome():
    # initial variables
    url = 'https://www.myhome.ge/ka/'
    curr_page = 1
    page = http.get(url + 'search?&Ajax=1&Page=' + str(curr_page)).json()['Data']
    page_count = round(int(page['Cnt']) / 22)  # total page count
    file_name = 'myhome-{}.csv'.format(datetime.now().__format__('%y-%m-%d_%H%M%S'))
    columns = [
        'UserID', 'Date', 'Type', 'Address', 'Floor', 'Rooms', 'Area (m²)',
        'Phone', 'Price', 'Images'
    ]

    pd.DataFrame(columns=columns).to_csv(file_name, index=False, sep=';', mode='a', header=True)

    # Progress bar
    with click.progressbar(range(1, page_count), label='Parsing myhome.ge', ) as bar:
        for i in bar:

            for product in page['Prs']:
                user_id = product['user_id']
                date = product['order_date']
                address = product['street_address']
                floor = product['floor']
                rooms = product['rooms']
                area = product['area_size']
                price = product['price']

                # grab details
                details = http.get(url + 'product?id=' + str(product['product_id']))
                soup = BeautifulSoup(details.content, 'html.parser')
                types = soup.select_one('div .statement-title h1').text.strip()
                phone = soup.select_one('span.number').text.strip()
                images = [i.get('data-background') for i in soup.select('div[data-background^=https://static.my.ge/myhome/photos/large/]')]

                pd.DataFrame({
                    'UserID': user_id,
                    'Date': date,
                    'Type': types,
                    'Address': str(address).replace(',', '.').replace(';', '.'),
                    'Floor': floor,
                    'Rooms': rooms,
                    'Area (m²)': area,
                    'Phone': phone,
                    'Price': price,
                    'Images': '\n'.join(images)
                }, index=['UserID'], columns=columns).to_csv(file_name, index=False, sep=';', mode='a', header=False)

            curr_page += 1


if __name__ == '__main__':
    run()
