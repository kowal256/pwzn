__author__ = 'dk'

import requests
from math import ceil
from multiprocessing import Pool
import hashlib


def get_range(args):
    url = args[0]
    rng = (args[1], args[2])
    print("Downloading {} - {}".format(*rng))
    data = requests.get(url, headers={"Range": "bytes={}-{}".format(*rng)})
    return data.content


def download(url, fragments):
    response = requests.head(url)
    len = int(response.headers['Content-Length'])
    print("length: {}".format(len))

    step = int(ceil(len/fragments))
    args = [(url, step*frag, min(len, step*frag+step-1)) for frag in range(fragments)]
    #print(ranges)

    pool = Pool(fragments)
    return b''.join(pool.map(get_range, args))


if __name__ == '__main__':
    data = download("http://db.fizyka.pw.edu.pl/pwzn-data/zaj7/rand-data-a", 4)
    hash = hashlib.md5()
    hash.update(data)
    print("MD5 of downloaded file: {}".format(hash.hexdigest()))
