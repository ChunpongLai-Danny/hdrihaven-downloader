# Download all hdris from hdrihaven

# Import modules
import requests
import os
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from urllib.request import urlretrieve
from urllib.request import URLopener
from fake_useragent import UserAgent

ua = UserAgent()
opener = URLopener()
opener.addheader('User-Agent', ua.chrome)

url = 'https://hdrihaven.com/hdris/'
category = 'all'
resolution = '2k'
url_category = url + '?c=' + category

r = requests.get(url_category, allow_redirects=True, headers={'User-Agent': ua.chrome})
soup = BeautifulSoup(r.text, 'html.parser')

save_to = 'hdri_' + resolution
try:
    os.mkdir(save_to)
except Exception as e:
    pass
os.chdir(save_to)

hdris = soup.select('#item-grid a')
#print(hdris)
for hdri in hdris:
    thumbnail = hdri.select('.thumbnail')[0]['data-src']
    href = urlparse(hdri['href'])
    filename = href.query[2:] + '_' + resolution

    # DL link example
    # https://hdrihaven.com/files/hdris/small_harbor_02_2k.hdr
    dl_url = (
        'https://hdrihaven.com/files/hdris/' + filename
    )
    thumbnail_url = 'https://hdrihaven.com' + thumbnail
    print(dl_url)
    print(thumbnail_url)

    try:
        print('downloading hdr...')
        ext = '.hdr'
        opener.retrieve(dl_url + ext, filename + ext)
    except Exception as e:
        print('hdr download failed, trying exr...')
        try:
            ext = '.exr'
            opener.retrieve(dl_url + ext, filename + ext)
        except Exception as e:
            print('download failed. Continuing...\n')
            continue
    print('')
    opener.retrieve(thumbnail_url, os.path.basename(thumbnail_url))

print('Done')
