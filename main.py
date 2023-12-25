import os
import requests
from bs4 import BeautifulSoup
import sys

page = 0
def get_user_input():
    search = input("Search for tags (if more than one separate by comma): ")
    tags = []
    if ',' in search:
        search = search.split(',')
        for tag in search:
            tag.strip()
        search = '+'.join(search)
    else:
        pass
    return search
def get_max_downloads():
    max_downloads = input('how many do you want to download?: ')
    
    return max_downloads
def get_soup(url, headers):
    response = requests.get(url, headers=headers)
    return BeautifulSoup(response.text, "html.parser")
def extract_image_links(soup, headers):
    a_tags = soup.select('article a')
    images = []
    lengt = len(a_tags)
    if lengt == 0:
        print('no images found, check spelling and try again.')
        sys.exit()
    print("scraping...")
    for a in a_tags:
        link = a['href']
        response = requests.get(link, headers=headers)
        soup_post = BeautifulSoup(response.text, "html.parser")
        img = soup_post.find('img', class_='fit-width')
        if img:
            image_url = img['src']
            images.append(image_url)
        else:
            print(f'''Can't find an image in: {link} (probably a video)''')
    return images
def download_images(links, search, page, headers, max_downloads):
    os.makedirs(search, exist_ok=True)
    downloaded = 0
    for link in links:
        response = requests.get(link)
        
        if response.status_code == 200:
            filename = os.path.join(search, link.split('/')[-1])
            with open(filename, 'wb') as file:
                file.write(response.content)
            print(f'Downloaded: {filename}')
            downloaded += 1
            print(f'downloaded: {downloaded}, max_downloads: {max_downloads}')
            if downloaded == max_downloads:
                print('done')
                sys.exit()
        elif response.status_code == 404:
            print(f'Image not found (404): {link}')
        else:
            print(f'Failed to download: {link} (Status Code: {response.status_code})')
            
    page += 42
    script_dir = os.path.dirname(os.path.abspath(__file__))
    download_dir = os.path.join(script_dir, search)
    next_page(search, page, headers)
def next_page(search, page, headers):
    print('going to the next page...')
    url = f"https://gelbooru.com/index.php?page=post&s=list&tags={search}+&pid={page}"
    soup = get_soup(url, headers)
    links = extract_image_links(soup, headers)
    download_images(links, search, page, headers, max_downloads)

def main(page):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    search = get_user_input()
    try:
        max_downloads = int(get_max_downloads())
    except ValueError:
        print('you should only Insert integer value.')
        sys.exit()
    url = f"https://gelbooru.com/index.php?page=post&s=list&tags={search}+&pid={page}"
    soup = get_soup(url, headers)
    links = extract_image_links(soup, headers)

    download_images(links, search, page, headers, max_downloads)

if __name__ == "__main__":
    try:
        main(page)
    except KeyboardInterrupt:
        exit()
