from vk_api import ApiException, GroupInfo, VkApi
import argparse
from typing import List


def select_groups(groups, at_once) -> List[GroupInfo]:
    """Returns list of selected groups"""
    selected = []
    for start in range(0, len(groups), at_once):
        for ind, g in enumerate(groups[start:start+at_once]):
            print(f'{ind + 1}. {g.name} ({g.url})')
        ids = list(
            map(int, input('Which one (write numbers separated with spaces)? ').split()))

        # transform relative indices to group
        selected += list(map(lambda id: groups[id + start - 1], ids))
    return selected


def get_confirmation(groups) -> bool:
    """Ask user for confirmation"""
    print('Chosen groups:')
    for ind, g in enumerate(groups):
        print(f'{ind + 1}. {g.name}')
    print(f'You will be unsubscribed from {len(groups)} groups.')
    return True if input('Are you sure? (y/n) ').lower() == 'y' else False


def save_to_csv(groups, filename='unsubscribed.csv', sep=','):
    with open(filename, 'w') as f:
        f.write(f'id{sep}name{sep}url\n')
        for g in groups:
            f.write(f'{g.id}{sep}{g.name}{sep}{g.url}\n')


def main(args):
    api = VkApi()
    groups = api.get_groups()
    selected = select_groups(groups, args.at_once)
    if not get_confirmation(selected):
        print('Aborting...')
        exit(0)
    error_counter = 0
    left = []
    for g in selected:
        try:
            api.leave_group(g.id)
            left.append(g)
            print(f'Successfully left "{g.name}" :)')
        except ApiException as e:
            error_counter += 1
            print(f'Cannot leave "{g.name} :("')
            print(f'Error message: {str(e)}')
    if args.to_csv:
        print('Saving to unsubscribed.csv...')
        save_to_csv(left)
    print(f'Total errors: {error_counter}. Bye')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--at_once", help="print that number of subscriptions at once", type=int, default=10)
    parser.add_argument(
        "--to_csv", help="save unsubscribed groups to csv file", default=False, action='store_true')
    main(parser.parse_args())
