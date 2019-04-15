# -*- coding: utf-8 -*-
import requests
import shutil
import urllib.request
import sys
from zipfile import ZipFile
import os
from urllib.error import HTTPError
from urllib.error import URLError

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
        content = page.read()
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

    sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percents, '%', suffix)),

    if iteration == total:
        sys.stdout.write('\n')
    sys.stdout.flush()

def create_dir(path):
    if os.path.exists(path):
        print('Directory %s already exists, all existing files will be skiped when downloading' % path)
        return True
    try:  
        os.mkdir(path)
    except OSError:  
        print ("Creation of the directory %s failed" % path)
        return False
    else:  
        print ("Successfully created the directory %s " % path)
        return True
