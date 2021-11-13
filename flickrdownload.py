import requests
from bs4 import BeautifulSoup
import random
import re
import json
import time
import flickrapi

class helps:
    def __init__(self):
        pass

    def __repr__(self):
        return 'You need other packages to run it. Using .packages to see the package requirements.'

class packages:
    def __init__(self):
        pass

    def __repr__(self):
        return 'requests, bs4, urllib, random, re, json and flickrapi'

class loginFlk:
    user_agent_list = ['Mozilla/5.0(compatible;MSIE9.0;WindowsNT6.1;Trident/5.0)',
            'Mozilla/4.0(compatible;MSIE8.0;WindowsNT6.0;Trident/4.0)',
            'Mozilla/4.0(compatible;MSIE7.0;WindowsNT6.0)',
            'Opera/9.80(WindowsNT6.1;U;en)Presto/2.8.131Version/11.11',
            'Mozilla/5.0(WindowsNT6.1;rv:2.0.1)Gecko/20100101Firefox/4.0.1',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER']

    def __init__(self, api_key, file_safe_pos):
        self.api_key = api_key
        self.file_safe_pos = file_safe_pos

    def download_single_album(self):
        album_link = input('enter the album\'s link... If finish entering, entering -1')
        link_get_setID = re.compile(r'albums/\d+')
        set_ID = link_get_setID.search(album_link).group()[7:]

        qsp = {
            "method": "flickr.photosets.getPhotos",
            "api_key": self.api_key,
            "photoset_id": set_ID,
            "format": "json",
            "nojsoncallback": "1"
        }

        header = loginFlk.user_agent_list[0]
        flickr_link = 'https://api.flickr.com/services/rest/'
        response = requests.get(flickr_link, params=qsp, headers={'user-agent': header})
        print('status code:', response.status_code)
        response_text = json.loads(response.text)
        photo_ids = []
        for i in range(len(response_text['photoset']['photo'])):
            photo_ids.append(response_text['photoset']['photo'][i]['id'])

        header = loginFlk.user_agent_list[0]
        photo_links = []
        for photo_id in photo_ids:
            #flickr_link = 'https://www.flickr.com/services/rest/'
            qsp = {
                "method": "flickr.photos.getSizes",
                "api_key": self.api_key,
                "photo_id": photo_id,
                "format": "json",
                "nojsoncallback": "1"
            }
            response2 = requests.get(flickr_link, params=qsp, headers={'user-agent': header})
            response2_text = json.loads(response2.text)
            for j in range(len(response2_text['sizes']['size'])):
                if response2_text['sizes']['size'][j]['label'] == 'Large 2048':
                    photo_links.append(response2_text['sizes']['size'][j]['source'])
                elif response2_text['sizes']['size'][j]['source'] == 'Large 1600':
                    photo_links.append(response2_text['sizes']['size'][j]['source'])
        print('CPU finished photo links collection')

        count = 0
        for photo_link in photo_links:
            header = random.choice(loginFlk.user_agent_list)
            response_img = requests.get(photo_link, headers={'user-agent': header}).content
            try:
                with open(self.file_safe_pos + photo_link[37:62] + '.jpg', 'wb') as image:
                    image.write(response_img)
                count += 1
                print('number ' + str(count) + ' img is successfully downloaded')
            except:
                count += 1
                print('number ' + str(count) + ' img failed to be downloaded')
        print('The whole download process is done')

    def download_multiple_albums(self):
        loginFlk.user_agent_list = ['Mozilla/5.0(compatible;MSIE9.0;WindowsNT6.1;Trident/5.0)',
            'Mozilla/4.0(compatible;MSIE8.0;WindowsNT6.0;Trident/4.0)',
            'Mozilla/4.0(compatible;MSIE7.0;WindowsNT6.0)',
            'Opera/9.80(WindowsNT6.1;U;en)Presto/2.8.131Version/11.11',
            'Mozilla/5.0(WindowsNT6.1;rv:2.0.1)Gecko/20100101Firefox/4.0.1',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER']

        album_links = []
        album_link = input("enter the album's link... If finish entering, entering -1")
        while album_link != '-1':
            album_links.append(album_link)
            album_link = input("enter the album's link... If finish entering, entering -1")

        for k in range(len(album_links)):
            try:
                link_get_setID = re.compile(r'albums/\d+')
                set_ID = link_get_setID.search(album_links[k]).group()[7:]
            except:
                print('false link')
                continue

            # 向flickr發出請求，要取得album裡面所有的photo id
            flickr_link = 'https://api.flickr.com/services/rest/'
            api_key = u'c980de221e5ddeb6adf71934e8a5fdc6'
            qsp = {
                "method": "flickr.photosets.getPhotos",
                "api_key": api_key,
                "photoset_id": set_ID,
                "format": "json",
                "nojsoncallback": "1"
            }
            header = loginFlk.user_agent_list[0]
            response = requests.get(flickr_link, params=qsp, headers={'user-agent': header})
            print('status code:', response.status_code)
            try:
                response_text = json.loads(response.text)
                photo_ids = []  # 取得photo id的容器
                for i in range(len(response_text['photoset']['photo'])):
                    photo_ids.append(response_text['photoset']['photo'][i]['id'])
            except:
                print("The photographer probably don't provide users to mine pictures")
                print("The album's link is {}".format(album_links[k]))
                continue

            # 再次向flickr發出請求，請求取得所有photo id 的live://staticflickr狀態的照片源頭檔案(也就是photo link)，同時做大小的篩選
            header = loginFlk.user_agent_list[0]
            photo_links = []
            for photo_id in photo_ids:
                flickr_link = 'https://www.flickr.com/services/rest/'
                qsp = {
                    "method": "flickr.photos.getSizes",
                    "api_key": self.api_key,
                    "photo_id": photo_id,
                    "format": "json",
                    "nojsoncallback": "1"
                }
                response2 = requests.get(flickr_link, params=qsp, headers={'user-agent': header})
                response2_text = json.loads(response2.text)
                for j in range(len(response2_text['sizes']['size'])):
                    if response2_text['sizes']['size'][j]['label'] == 'Large 2048':
                        photo_links.append(response2_text['sizes']['size'][j]['source'])
                    elif response2_text['sizes']['size'][j]['source'] == 'Large 1600':
                        photo_links.append(response2_text['sizes']['size'][j]['source'])
            print('CPU finished photo links collection')

            # 把上一步蒐集到的所有相簿的photo links，拿出來一個一個下載
            count = 0
            for photo_link in photo_links:
                header = random.choice(loginFlk.user_agent_list)
                response_img = requests.get(photo_link, headers={'user-agent': header}).content
                try:
                    with open(self.file_safe_pos + photo_link[37:62] + '.jpg', 'wb') as image:
                        image.write(response_img)
                    count += 1
                    print('number ' + str(count) + ' img is successfully downloaded')
                except:
                    count += 1
                    print('number ' + str(count) + ' img failed to be downloaded')
            time.sleep(3)
            print("The number {} album finished downloading".format(k + 1))
        print('The whole download process is done')

    def download_respective_photo(self):
        photo_panels = []
        img_link = input('entering the photo\'s link... If finish entering, entering -1')
        while img_link != '-1':
            photo_panels.append(img_link)
            img_link = input()

        photo_ids2 = []
        for photo_panel in photo_panels:
            try:
                img_id_search = re.compile(r'(\d+)/in')
                img_id = img_id_search.search(photo_panel).group(0)[:-3]
                photo_ids2.append(img_id)
            except:
                print('there are something wrong')

        photo_links2 = []
        count = 0
        for i in range(len(photo_ids2)):
            api_key = u'c980de221e5ddeb6adf71934e8a5fdc6'
            api_secret = u'607aadf2e58f040b'
            url = 'https://www.flickr.com/services/rest/'
            header = 'Mozilla/4.0(compatible;MSIE8.0;WindowsNT6.0;Trident/4.0)'
            qsp = {
                "method": "flickr.photos.getSizes",
                "api_key": self.api_key,
                "photo_id": photo_ids2[i],
                "format": "json",
                "nojsoncallback": "1"
            }
            response3 = requests.get(url, headers={'user-agent': header}, params=qsp)
            response3_text = json.loads(response3.text)
            for j in range(len(response3_text['sizes']['size'])):
                if response3_text['sizes']['size'][j]['label'] == 'Large 2048':  # 1600 or 2048
                    photo_links2.append(response3_text['sizes']['size'][j]['source'])
        #         elif response3_text['sizes']['size'][j]['source'] == 'Large 1600':
        #             photo_links2.append(response3_text['sizes']['size'][j]['source'])
        print('CPU finished photo links collection')

        for photo_link2 in photo_links2:
            header = random.choice(loginFlk.user_agent_list)
            response_img2 = requests.get(photo_link2, headers={'user-agent': header}).content
            try:
                with open(self.file_safe_pos + photo_link2[37:62] + '.jpg', 'wb') as image:
                    image.write(response_img2)
                count += 1
                print('number ' + str(count) + ' img is successfully downloaded')
            except:
                count += 1
                print('number ' + str(count) + ' img failed to be downloaded')
        print('The whole download process is done')

    def violent_crawling(self):
        print('Warning!! Violent crawling may not crawl all of the information on the internet.')
        url = input('entering your album\'s link...')
        header = random.choice(loginFlk.user_agent_list)
        response = requests.get(url, headers={'user-agent': header})
        response_text = response.text
        soup = BeautifulSoup(response_text, 'html.parser')

        html_code = soup.find_all('html')
        html_text = str(html_code)

        url_compile = re.compile(r'live.staticflickr.com\W\W\d+\W\W\d\d\d\d\d\d\d\d\d\d\d_\w\w\w\w\w\w\w\w\w\w_k.jpg')
        url_list_org = url_compile.findall(html_text)
        url_list = []
        for urls in url_list_org:
            if urls[-5] == 'k':
                urls = urls.replace('\\', '/')
                url_list.append(urls)
            elif urls[-5] == 'h':
                urls = urls.replace('\\', '/')
                url_list.append(urls)

        for i in range(len(url_list)):
            img_url = 'https://' + url_list[i]
            if i > 0:
                if url_list[i] == url_list[i - 1]:
                    continue
            try:
                header = random.choice(loginFlk.user_agent_list)
                # header = 'Mozilla/5.0(WindowsNT6.1;rv:2.0.1)Gecko/20100101Firefox/4.0.1'
                response = requests.get(img_url, headers={'user-agent': header}).content
                with open(self.file_safe_pos + img_url[37:62] + '.jpg', 'wb') as file:
                    file.write(response)
                time.sleep(1)
                print('successfully download {}'.format(i))
            except:
                print('Number {} picture failed to downloaded'.format(i))
        print('If you did not find the images, this may be: 1. Photographer did not provide same size pictures as you indicated, 2. phtographer did not allow people withoit membership to see, 3. other problem')

