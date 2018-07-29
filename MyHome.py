import csv
import requests as http
from datetime import datetime
from bs4 import BeautifulSoup


class Grab:
    now = datetime.now().__format__('%y-%m-%d_%H:%M:%S')

    def __init__(self, url, page, products, curr_page=1):
        self.url = url
        self.products = products
        self.currPage = curr_page
        self.page = page
        return

    def run(self):
        # product loop
        with open('myhome-{}.csv'.format(self.now), 'w+') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=[
                'UserID', 'Date', 'Type', 'Address', 'Floor', 'Rooms', 'Area (m²)',
                'Price', 'Phone', 'Images'
            ])
            writer.writeheader()
            for product in self.products:
                user_id = product['user_id']
                date = product['order_date']
                address = product['street_address']
                floor = product['floor']
                rooms = product['rooms']
                area = product['area_size']
                price = product['price']

                # grab details
                details = http.get(self.url + 'product?id=' + str(product['product_id']))
                soup = BeautifulSoup(details.content, 'html.parser')
                type = soup.select_one('div .statement-title h1').text.strip()
                images = [i.get('data-background') for i in soup.select('div[data-background^=https://static.my.ge/myhome/photos/large/]')]
                phone = soup.select_one('span.number').text.strip()

                writer.writerow(
                    {
                        'UserID': user_id,
                        'Date': date,
                        'Type': type,
                        'Address': address,
                        'Floor': floor,
                        'Rooms': rooms,
                        'Area (m²)': area,
                        'Price': price,
                        'Phone': phone,
                        'Images': '|'.join(images)
                    }

                )
