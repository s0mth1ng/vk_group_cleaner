from os import pardir
from vk_api import VkApi
import argparse
from typing import List


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--at_once", help="print that number of subscriptions at once", type=int, default=10)
    return parser.parse_args()


def select_groups(groups, at_once) -> List[int]:
    """Returns list of selected groups"""
    selected = []
    for start in range(0, len(groups), at_once):
        for ind, g in enumerate(groups[start:start+at_once]):
            print(f'{ind + 1}. {g.name} ({g.url})')
        ids = list(
            map(int, input('Which one (write numbers separated with spaces)? ').split()))

        # transform relative indices to group
        ids = list(map(lambda id: groups[id + start - 1], ids))
        selected += ids
    return selected


def get_confirmation(groups) -> bool:
    """Ask user for confirmation"""
    print('Chosen groups:')
    for ind, g in enumerate(groups):
        print(f'{ind + 1}. {g.name}')
    print(f'You will be unsubscribed from {len(groups)} groups.')
    return True if input('Are you sure? (y/n) ').lower() == 'y' else False


def main():
    api = VkApi()
    groups = api.get_groups()
    args = get_args()
    selected = select_groups(groups, args.at_once)


if __name__ == '__main__':
    main()
