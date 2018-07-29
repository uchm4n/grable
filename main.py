import click
import requests as http
from MyHome import Grab


@click.group()
def run():
    pass


@run.command(help='A command to get data from myhome.ge')
def myhome():
    url = 'https://www.myhome.ge/ka/'
    curr_page = 1
    page = http.get(url + 'search?&Ajax=1&Page=' + str(curr_page)).json()['Data']
    page_count = round(int(page['Cnt']) / 22)  # total page count

    # Progress bar
    with click.progressbar(range(1, page_count), label='Parsing myhome.ge', ) as bar:
        for i in bar:
            Grab(url, page, products=page['Prs'], curr_page=curr_page).run()
            curr_page += 1


if __name__ == '__main__':
    run()
