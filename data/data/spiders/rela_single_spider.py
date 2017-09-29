import sys
sys.path.append('..')
import database.sql as sql
import json
import scrapy
import time
import itertools
from scrapy import Request
import random
'''	
    Common method for getting a signle items based on the relationship file
    Each method need a param s that represents a spider object
'''

token_list = [
''' Put your own token list here '''
]
token_iter = itertools.cycle(token_list)
handle_httpstatus_list = [401,403,404,451,422]
time_inter = 60

def init_all_item(s):
    print "Init items data..."
    s.all_item = list(sql.select(s.src_table, s.src_key))
    random.shuffle(s.all_item)
    s.cur_item_ind = 0
    s.cur_item = s.all_item[s.cur_item_ind][s.src_key[0]]
    sql.delete(s.des_table, s.des_key[0], s.cur_item)

def get_next_item(s):
    s.cur_item_ind += 1
    if s.cur_item_ind < len(s.all_item):
        s.cur_item = s.all_item[s.cur_item_ind][s.src_key[0]]
        sql.delete(s.des_table, s.des_key[0], s.cur_item)
    else:
        init_all_item(s)

def get_url(s):
    url = s.base_url + s.cur_item
    return url

def get_headers(s):
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:36.0) Gecko/20100101 Firefox/36.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en',
        'Authorization': 'token ' + token_iter.next(),
    }
    return headers

# method for generating the first crawl request
def start_requests(s):
    init_all_item(s)    
    print("---------- Index [%d] [%s] ----------"%(s.cur_item_ind, s.cur_item))
    return [Request(get_url(s), headers=get_headers(s), callback=s.parse, dont_filter=True)]

# method for yielding the next crawl request 
def yield_request(s):
    print("---------- Index [%d] [%s] ----------"%(s.cur_item_ind, s.cur_item))
    return Request(get_url(s), headers=get_headers(s), callback=s.parse, dont_filter=True)

def do_item_parse(s, res):
    user = json.loads(res.body_as_unicode())
    for i in range(len(s.des_key)):
        s.des_val[s.des_key[i]] = user[s.des_key[i]]
    for i in range(len(s.des_2key)):
        s.des_val[s.des_2key[i]] = user[s.res_1key[i]][s.res_2key[i]]
    sql.insert(s.des_table, s.des_val)

# method for handling for error
def handle_error(s, res):
    print("* Meet an error [%d] *"%res.status)
    if res.status == 403:
        print("* Rate limit and wait for [%d] s... *"%s.time_inter)
        time.sleep(s.time_inter)
    if False:
        s.error_time += 1
        if s.error_time >= len(token_list):
            print("* Rate limit and wait for [%d] s... *"%s.time_inter)
            time.sleep(s.time_inter)
            s.error_time = 0
