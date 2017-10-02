import sys
sys.path.append('..')
import database.sql as sql
import json
import scrapy
import time
import itertools
from scrapy import Request
import random
import sqs_send
import os
''' 
    Common method for getting a relationship based on the single
    Each method need a param s that represents a spider object
'''

token_list = os.environ['GITHUB_TOKENS'].split(':')

token_iter = itertools.cycle(token_list)
handle_httpstatus_list = [401,403,404,451,422]
time_inter = 60

def init_all_item(s):
    print "Init items data..."
    res = sql.select(s.src_table, s.src_key)
    if res:
        s.all_item = list(res)
    else:
        s.all_item = []
        print "No Data, wait for 5 s"
        time.sleep(5)
    random.shuffle(s.all_item)
    s.cur_item_ind = 0
    if(s.cur_item_ind < len(s.all_item)):
        s.cur_item = s.all_item[s.cur_item_ind][s.src_key[0]]
    s.des_val[s.des_key[0]] = s.cur_item
    sql.delete(s.des_table, s.des_key[0], s.cur_item)
    s.page_num = 1
    s.rela_num = 0
    
# method for getting next item index from the single items table
def get_next_item(s):
    if s.page_num == 1:
        s.cur_item_ind += 1
        if s.cur_item_ind < len(s.all_item):
            s.cur_item = s.all_item[s.cur_item_ind][s.src_key[0]]
            s.des_val[s.des_key[0]] = s.cur_item
            sql.delete(s.des_table, s.des_key[0], s.cur_item)
            s.page_num = 1
            s.rela_num = 0
        else:
            init_all_item(s)

def get_url(s):
    url = s.base_url + s.cur_item + "/" + s.url_rela_name + "?page="+str(s.page_num)+"&per_page="+str(s.per_page)
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
    return [Request(get_url(s), headers=get_headers(s), callback=s.parse,dont_filter=True)]

# method for yielding the next crawl request
def yield_request(s):
    if s.page_num == 1:
        print("---------- Index [%d] [%s] ----------"%(s.cur_item_ind, s.cur_item))
    return Request(get_url(s), headers=get_headers(s), callback=s.parse, dont_filter=True)

# method for handling the data back from the request
def do_item_parse(s, res):
    relas = json.loads(res.body_as_unicode())
    s.des_val[s.des_key[1]] = []
    for rela in relas:
        s.des_val[s.des_key[1]].append(rela[s.rela_key])
    sqs_send.send(s.des_table,s.des_val,'single_rela',s.des_key[0],s.des_key[1])
        #sql.insert(s.des_table, s.des_val) 
    s.rela_num += len(relas)
    if len(relas) == s.per_page:
        s.page_num += 1
    elif len(relas) < s.per_page:
        print("++++++++++ [%s] with [%d] %s ++++++++++"%(s.cur_item, s.rela_num, s.url_rela_name))
        s.page_num = 1

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

