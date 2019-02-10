from bs4 import BeautifulSoup
import requests
import sys

'''Create a map of the domain for Clarence'''

if len(sys.argv) > 1:
    base_address = sys.argv[1]
else:
    base_address = 'http://127.0.0.1:8000'

# http://127.0.0.1:8000
# http://0.0.0.0:8000

# check - if url doesn't end with '/', it can cause problems while adding path - for example /other_site
if base_address.endswith('/'):
    base_address = base_address[0:len(base_address)-1]

pages_todo = set()
pages_todo.add(base_address)

pages_done = {}


def check_address(address):
    pages_done[address] = {'title': '', 'links': set()}

    try:
        source = requests.get(address).text
    except Exception as error:
        # many errors may happen: ConnectionError, MissingSchema etc
        pages_done[address]['error'] = error
    else:
        # parse html text
        soup = BeautifulSoup(source, 'lxml')

        pages_done[address]['title'] = soup.find('title').text

        for a in soup.find_all('a', href=True):

            if a['href'].startswith('/'):
                link = base_address + a['href']
                pages_done[address]['links'].add(link)

            elif base_address in a['href']:
                pages_done[address]['links'].add(a['href'])


def print_pages():
    for address in pages_done:
        print(f'{address}: ')
        for element in pages_done[address]:
            print(f'{element}: {pages_done[address][element]}')
        print()


def check_all_pages_from_todo():

    while len(pages_todo) > len(pages_done):

        for address in pages_todo:
            if address not in pages_done:
                check_address(address)

        # can't change iterator while iterate for it, so second 'for' to update pages_todo
        for address in pages_done:
            for link in pages_done[address]['links']:
                pages_todo.add(link)

    print_pages()


if __name__ == '__main__':
    check_all_pages_from_todo()
