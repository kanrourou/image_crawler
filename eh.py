# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import sys
import utils

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

def download(site):
    html = utils.get_html(site)
    metadata = get_gallery_metadata(html)
    urls = get_page_urls(html)
    sections = metadata["Length"].split()
    total_images = int(sections[0])
    title = metadata["Title"]
    utils.create_dir(title)
    utils.print_progress(0, total_images)
    i = 0

    for url in urls:
        page_html = utils.get_html(url)
        image_urls = get_image_urls(page_html)
        for image_url in image_urls:
            image_page_html = utils.get_html(image_url)
            image_src = get_image_src(image_page_html)
            parts = image_src.split('.')
            extension = ('.' + parts[-1] if parts[-1]  else '.jpg') if parts else  '.jpg'
            utils.get_image(image_src, title + '/' + get_file_name(total_images, i + 1) + extension)
            i += 1
            utils.print_progress(i, total_images)


site = sys.argv[1]
download(site)
