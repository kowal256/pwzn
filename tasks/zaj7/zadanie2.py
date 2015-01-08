__author__ = 'dk'

import requests
import argparse
from math import ceil
from multiprocessing import Pool, Queue, Process
import hashlib
import bs4


def get_links(page):
    if page[1] >= 5:
        return []
    else:


def crawl(session, visited, to_go):
    while True:
        page = to_go.get()

        for link in get_links(page):
            visited.put(link)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('host', help='host')
    parser.add_argument('port')
    parser.add_argument('N', help='Number of processes')

    args = parser.parse_args()

    s = requests.Session()
    s.post("{}/{}/login".format(args.host, args.port), {'user': 'foo', 'password': 'bar'})

    visited, to_go = Queue(), Queue()
    to_go.put((0, "{}:{}/12345niepamietam".format(args.host, args.port)))

    #fhgfhgfhggfh


