import re
import requests

TOKEN = "SAMPLE TOKEN"

GAS = "https://vk.com/album-6923031_264590399"

LG = "https://vk.com/album-288_256660479"

class VKFindInAlbum:

    def __init__(self, access_token, album_url=''):
        self.access_token = access_token
        self.album_url = album_url

    def __get_photos_item_list(self, url):
        r = requests.get(url)
        data = r.json()
        result = data['response']['items']
        return result

    def __get_comments_item_list(self, url):
        r = requests.get(url)
        data = r.json()
        count = data['response']['count']
        result = data['response']['items']
        if count > 100:
            i = 100
            while i < count:
                api_url = f'{url}&offset={i}'
                r = requests.get(api_url)
                data = r.json()
                result.extend(data['response']['items'])
                i += 100
                print(i)
        return result

    def __get_album_id(self, album_url):
        album_id = re.search(r'\d+$', album_url)
        album_id = album_id[0]
        return album_id
    
    def __get_group_id(self, album_url):
        group_id = re.search(r'\d+', album_url)
        group_id = group_id[0]
        return group_id

    def __prepare_api_photos_call(self, album_url):
        group_id = self.__get_group_id(album_url)
        album_id = self.__get_album_id(album_url)
        api_url = f'https://api.vk.com/method/photos.get?v=5.101&access_token={self.access_token}&owner_id=-{group_id}&album_id={album_id}&count=1000&extended=1'

        return api_url

    def __prepare_api_album_comments_call(self, album_url, offset=0):
        group_id = self.__get_group_id(album_url)
        album_id = self.__get_album_id(album_url)
        api_url = f'https://api.vk.com/method/photos.getAllComments?v=5.101&access_token={self.access_token}&owner_id=-{group_id}&album_id={album_id}&count=100'

        return api_url

    def __find_string_in_list(self, list, string):
        result = []
        for item in list:
            text = item['text'].lower()
            if text.find(string.lower()) != -1:
                result.append(item)

        return result

    def prepare_photo_urls_from_descriptions(self, album_url, string):
        api_url = self.__prepare_api_photos_call(album_url)
        item_list = self.__get_photos_item_list(api_url)
        photos_list = self.__find_string_in_list(item_list, string)
        result = self.__prepare_photos_ulrs(photos_list)

        return result

    def prepare_photo_urls_from_comments(self, album_url, string):
        api_url = self.__prepare_api_album_comments_call(album_url)
        item_list = self.__get_comments_item_list(api_url)
        comment_list = self.__find_string_in_list(item_list, string)
        result = self.__prepare_photos_ulrs(comment_list, is_comments=True, album_url=album_url)
        
        return result

    def get_all_photos(self, album_list, string):
        result = []
        for item in album_list:
                        

    def __prepare_photos_ulrs(self, list, is_comments=False, album_url=''):
        result = []
        for item in list:
            if is_comments:
                id = item['pid']
                group_id = self.__get_group_id(album_url)
            else:
                id = item['id']
                group_id = abs(item['owner_id'])
            url = f'https:/vk.com/photo-{group_id}_{id}'
            result.append(url)
        return result



a = VKFindInAlbum(TOKEN)

b = a.prepare_photo_urls_from_descriptions(GAS, 'esp')

for i in b:
    print(i)
