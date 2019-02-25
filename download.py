
from utils import *
import os
from multiprocessing import Pool

def down(url):
    os.system('youtube-dl {}'.format(url))

def get_video():
    res = read_mongo({'is_video': 'true'})
    lis = res[:20]

    groups =  [item['url'] for item in lis]
    pool = Pool()
    pool.map(down,groups)

        
if __name__ == '__main__':
    get_video()