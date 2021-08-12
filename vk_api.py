import requests
from typing import List
from collections import namedtuple
from urllib.parse import urlparse, parse_qs


GroupInfo = namedtuple('GroupInfo', ['id', 'name', 'url'])


class ApiException(Exception):
    """Class for variety api errors"""
    pass


class VkApi:

    def __authorize(self) -> str:
        """Returns user token and saves user id"""
        url = 'https://oauth.vk.com/authorize'
        data = {
            'client_id': '7924582',
            'redirect_uri': 'https://oauth.vk.com/blank.html',
            'scope': 'groups',
            'response_type': 'token'
        }
        go_to = requests.Request('GET', url, data).prepare().url
        print(f'First of all you need to authorize.\n\n1. Go to {go_to}')
        token_url = input(
            'Authorize and paste below the url of the page you\'ve been redirected to\n')
        parsed = parse_qs(urlparse(token_url).fragment)
        self.__uid = int(parsed['user_id'][0])
        return parsed['access_token'][0]

    def __init__(self):
        self.__default_params = {
            'access_token': self.__authorize(),
            'v': 5.131
        }
        self.__url = 'https://api.vk.com/method/'

    def __send_request(self, method: str, data: dict):
        """Returns response parsed json object"""
        url = f'{self.__url}{method}'
        try:
            r = requests.get(url, {**data, **self.__default_params})
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)
        return r.json()

    def get_groups(self) -> List[GroupInfo]:
        data = self.__send_request(
            'groups.get', {'user_id': self.__uid, 'extended': True})
        try:
            items = data['response']['items']
            return [GroupInfo(i['id'], i['name'],
                              f"https://vk.com/{i['screen_name']}") for i in items]
        except KeyError:
            raise ApiException('Incorrect user id')

    def leave_group(self, gid: int) -> None:
        data = self.__send_request('groups.leave', {'group_id': gid})
        if data.get('response', 0) != 0:
            raise ApiException(data['error']['error_msg'])
