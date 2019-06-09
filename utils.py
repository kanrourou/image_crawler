# -*- coding: utf-8 -*-
import requests
import shutil
import urllib.request
import sys
import os
from urllib.error import HTTPError
from urllib.error import URLError
import http.cookiejar

# Use urllib with header can avoid ip address ban
def get_html(url):
    try:
        hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                'Accept-Encoding': 'none',
                'Accept-Language': 'en-US,en;q=0.8',
                'Connection': 'keep-alive'}
        req = urllib.request.Request(url, headers=hdr)
        page = urllib.request.urlopen(req)
        content = page.read().decode('utf-8')
        abort_if_banned(content)
        return content
    except (HTTPError, URLError) as error:
        return ''

# If the content is offensive
# Warning only happens on gallery page
def is_warning_page(html):
    html = html.lower()
    warning = 'content warning'
    offensive = 'offensive for everyone'
    if html.find(warning) != -1 and html.find(offensive) != -1:
        #print('The page has offensive content...')
        return True
    else:
        return False

# If banned, we can only abort
def abort_if_banned(html):
    banned = 'your ip address has been temporarily banned'
    html = html.lower()
    if html.find(banned) != -1:
        print(html)
        exit(1)

def get_cookies(url):
    try:
        cj = http.cookiejar.CookieJar()
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
        opener.addheaders = [
                ('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'),
                ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
                ('Accept-Charset', 'ISO-8859-1,utf-8;q=0.7,*;q=0.3'),
                ('Accept-Encoding', 'none'),
                ('Accept-Language', 'en-US,en;q=0.8'),
                ('Connection', 'keep-alive'),
                ]
        urllib.request.install_opener(opener)
        req = urllib.request.Request(url)
        resp = urllib.request.urlopen(req)
        if(resp.status == 200):
            print('Successfully retrieved cookies')
            return cj
        else:
            print("Failed to retrieve cookies")
            exit(1)
    except (HTTPError, URLError) as error:
        print("Failed to retrieve cookies")
        exit(1)

# get around warning page by settig cookies
def get_html_with_cookies(url, cj):
    try:
        url += '?nw=always'
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
        opener.addheaders = [
                ('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'),
                ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
                ('Accept-Charset', 'ISO-8859-1,utf-8;q=0.7,*;q=0.3'),
                ('Accept-Encoding', 'none'),
                ('Accept-Language', 'en-US,en;q=0.8'),
                ('Connection', 'keep-alive'),
                ]
        urllib.request.install_opener(opener)
        req = urllib.request.Request(url)
        resp = urllib.request.urlopen(req)
        content = resp.read().decode('utf-8')
        abort_if_banned(content)
        return content
    except (HTTPError, URLError) as error:
        return ''

def get_image(url, path):
    try:
        with urllib.request.urlopen(url) as response, open(path, 'wb') as out_file:
            data = response.read()
            out_file.write(data)
    except (HTTPError, URLError) as error:
        return False
    else:
        return True

# Print iterations progress
def print_progress(iteration, total, prefix='Progress::', suffix='Complete', decimals=1, bar_length=100):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        bar_length  - Optional  : character length of bar (Int)
    """
    str_format = "{0:." + str(decimals) + "f}"
    percents = str_format.format(100 * (iteration / float(total)))
    filled_length = int(round(bar_length * iteration / float(total)))
    bar = '█' * filled_length + '-' * (bar_length - filled_length)

    sys.stdout.write('\r{} |{}| {}{} {}'.format(prefix, bar, percents, '%', suffix)),
    if iteration == total:
        sys.stdout.write('\n')
    sys.stdout.flush()


def create_dir(path):
    if os.path.exists(path):
        print('Directory %s already exists, all existing files will be skiped when downloading' % path)
        return True
    try:  
        os.mkdir(path)
    except OSError as error:
        print(error)
        print ("Creation of the directory %s failed" % path)
        return False
    else:  
        print ("Successfully created the directory %s " % path)
        return True
