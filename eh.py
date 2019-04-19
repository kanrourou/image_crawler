# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import sys
import utils
import time
import os

def get_page_urls(html):
    soup = BeautifulSoup(html, 'html.parser')
    href = soup.body.div.find_next_siblings('div')[2].find_all('a')[0]['href']
    last_page = soup.body.div.find_next_siblings('div')[2].find_all('td')[-2].a.get_text()
    num_of_pages = int(last_page)
    urls = [href]
    for page in range(1, num_of_pages): 
        urls.append(href + '?p=' + str(page))
    return urls

def get_gallery_metadata(html):
    soup = BeautifulSoup(html, 'html.parser')
    #number of webpages
    last_page = soup.body.div.find_next_siblings('div')[2].find_all('td')[-2].a.get_text()
    num_of_pages = int(last_page)
    #title
    title = soup.find(id = 'gn').get_text()
    #japanese title
    jap_title = soup.find(id = 'gj').get_text()
    metadata = {"Pages" : num_of_pages,
                'Title' : title,
                'Japanese Title' : jap_title}
    attrs = soup.findAll("td", {"class": "gdt1"})
    vals = soup.findAll("td", {"class": "gdt2"})
    cnt = len(attrs)
    for i in range(0, cnt):
        attr = attrs[i].get_text()[:-1]
        metadata[attr] = vals[i].get_text()
    return metadata

def get_image_src(html):
    soup = BeautifulSoup(html, 'html.parser')
    img_element = soup.find(id='img')
    return img_element['src']

def get_image_urls(html):
    soup = BeautifulSoup(html, 'html.parser')
    elements = soup.find(id='gdt').find_all('a')
    urls = []
    for element in elements:
        urls.append(element['href'])
    return urls

def get_file_name(total_images, idx):
   total_length = len(str(total_images))
   filled_length = len(str(idx))
   return '0' * (total_length - filled_length) + str(idx)

def print_metadata(data):
    for key,value in data.items():
        if(key == 'Pages'):
            continue
        print(key + ' : ' + value)

def download_gallery(site):
    start = time.time()
    html = utils.get_html(site)
    if not html:
        print('Failed to retrieve gallery page, process will be aborted!')
        return
    metadata = get_gallery_metadata(html)
    urls = get_page_urls(html)
    sections = metadata["Length"].split()
    total_images = int(sections[0]) if sections else 0
    title = metadata["Title"]
    print('Below is the informaiton of the gallery...')
    print_metadata(metadata)
    print('Start downloading...')
    title = title.replace('/', ' of ')
    if not utils.create_dir(title):
        return
    if total_images:
        utils.print_progress(0, total_images)
    else:
        print("Failed to get total number of images, progress bar is disabled!")
    i = 0
    img_fails = []
    gallery_page_fails = []
    img_page_fails = []

    #download images in each gallery page
    for url in urls:
        page_html = utils.get_html(url)
        if not page_html:
            gallery_page_fails.append(url)
            continue
        image_urls = get_image_urls(page_html)
        for image_url in image_urls:
            image_page_html = utils.get_html(image_url)
            if not image_page_html:
                img_page_fails.append(image_url)
                continue
            image_src = get_image_src(image_page_html)
            parts = image_src.split('.')
            extension = ('.' + parts[-1] if parts[-1]  else '.jpg') if parts else  '.jpg'
            file_name = get_file_name(total_images, i + 1) + extension
            file_path = title + '/' + file_name
            if not os.path.exists(file_path):
                if not utils.get_image(image_src, file_path):
                    img_fails.append(file_name)
            i += 1
            if total_images:
                utils.print_progress(i, total_images)

    #downloading result
    succeed = True
    if gallery_page_fails or img_page_fails:
        succeed = False
        print('Failed to load following pages:')
        for url in gallery_page_urls:
            print(url)
        for url in img_page_fails:
            print(url)
    if img_fails:
        succeed = False
        print('Failed to download following %s files...' % len(img_fails))
        for img in img_fails:
            print(img)
    if succeed:
        print('All files are downloaded successfully!')
    end = time.time()
    hours, rem = divmod(end-start, 3600)
    minutes, seconds = divmod(rem, 60)
    print("Total time elapsed {:0>2}m:{:02.0f}s".format(int(hours) * 60 + int(minutes),seconds))
     

site = sys.argv[1]
download_gallery(site)
