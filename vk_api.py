import requests
from typing import List
from collections import namedtuple
import re


GroupInfo = namedtuple('GroupInfo', ['id', 'name', 'url'])


class ApiException(Exception):
    """Class for variety api errors"""
    pass


class VkApi:

    def __authorize(self) -> str:
        """Returns user token"""
        url = 'https://oauth.vk.com/authorize'
        data = {
            'client_id': 7924582,
            'redirect_uri': 'https://oauth.vk.com/blank.html',
            'scope': 'groups',
            'response_type': 'token'
        }
        go_to = requests.Request('GET', url, data).prepare().url
        print(f'First of all you need to authorize.\n\n1. Go to {go_to}')
        token_url = input(
            'Authorize and paste below the url of the page you\'ve been redirected to\n')
        match = re.search(r'access_token=(\w+)&', token_url)
        if match is None:
            raise ValueError("Url does not contain access token.")
        return match.group(0)

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

    def get_user_id(self, user: str) -> int:
        data = self.__send_request('users.get', {'user_ids': user})
        try:
            return data['response'][0]['id']
        except KeyError:
            raise ApiException("User not found.")

    def get_groups(self, uid: int) -> List[GroupInfo]:
        data = self.__send_request(
            'groups.get', {'user_id': uid, 'extended': True})
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
