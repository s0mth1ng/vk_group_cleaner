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
    # TODO: write selective mechanism
    return []


def main():
    api = VkApi()
    groups = api.get_groups()
    args = get_args()
    selected = select_groups(groups, args.at_once)


if __name__ == '__main__':
    main()
