import json
import scrapy
import rela_single_spider as rss
'''	
	class for crawling user list by user_follow.txt 
	where store the relationship between user and thier followers
	and store the result to file user.txt
'''
class FollowedUserSpider(scrapy.spiders.Spider):
    name = "followed_user"
    allowed_domains = ["github.com"]
    src_table = 'user_user'
    src_key = ['followed']
    des_table = 'user'
    des_key = ['login','id','type','name','company','location','public_repos','public_gists','followers','following','created_at','updated_at']
    des_2key = []
    des_val = {}
    cur_item = ''
    cur_item_ind = 0
    all_item = []
    base_url = "https://api.github.com/users/"
    error_time = 0
    time_inter = rss.time_inter
    handle_httpstatus_list = rss.handle_httpstatus_list

    def __init__(self):
        scrapy.spiders.Spider.__init__(self)

    def __del__(self):
        self.item_file.close()
        self.rela_file.close()
    
    def start_requests(self):
        return rss.start_requests(self)

    def parse(self, response):
        if response.status in self.handle_httpstatus_list:
            rss.handle_error(self, response)
        else:
            self.error_time = 0
            rss.do_item_parse(self, response)
        rss.get_next_item(self)
        yield rss.yield_request(self)

