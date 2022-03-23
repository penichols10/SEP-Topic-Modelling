import requests
from bs4 import BeautifulSoup as bs
from tqdm import tqdm
import time
import os
from unidecode import unidecode

print(os.listdir())
NUM_DOCS = 3000
directory = 'pages//'
docs = []

def clean_filename(filename):
    filename = unidecode(filename)
    bad_chars = ['‘', '\'']
    for char in bad_chars:
        if char in filename:
            print(filename)
            filename = filename.replace(char, '')
    return filename

while len(os.listdir('pages//')) < NUM_DOCS:
    # load a page
    url = 'https://plato.stanford.edu/cgi-bin/encyclopedia/random'
    page = requests.get(url)
    soup = bs(page.content, 'html.parser')

    # Locate the title and clean it up
    # Every title contains the name of the site, so that is removed
    # Forward slashes are replaced with dashes
    title = ' '.join(soup.title.text.strip('\n').split()[:-4]).replace('/', '-')
    title = clean_filename(title)
    # Save the body of the document
    if title not in docs:
        docs.append(title)
        body = soup.find('div', id='main-text')
        # A minority of pages did not have anything in the body
        if body:
            paragraphs = '\n'.join([paragraph.text.strip('\n') for paragraph in body.find_all('p')])
            with open(f'{directory+title}.txt', 'w', encoding='utf8') as f:
                for paragraph in paragraphs:
                    f.write(paragraph)
    count = len(os.listdir('pages//'))
    if not count % 500:
        print(count)


    # sleep to be nice
    time.sleep(1)
