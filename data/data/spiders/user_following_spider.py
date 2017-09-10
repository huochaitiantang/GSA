import scrapy
import single_rela_spider as srs
''' 
    class for crawling followed people that user following and user relationship by user.txt 
    where store the user list
    and store the result to file user_following.txt
'''
class UserFollowingSpider(scrapy.spiders.Spider):
    name = "user_following"
    allowed_domains = ["github.com"]
    src_table = 'user'
    src_key = ['login']
    des_table = 'user_user'
    des_key = ['following','followed']
    des_val = {}
    url_rela_name = 'following'
    rela_key = 'login'
    rela_num = 0
    cur_item_ind = 0
    cur_item = ''
    all_item = []
    page_num = 1
    per_page = 100
    base_url = "https://api.github.com/users/"
    error_time = 0
    time_inter = srs.time_inter
    handle_httpstatus_list = srs.handle_httpstatus_list

    def __init__(self):
        scrapy.spiders.Spider.__init__(self)

    def __del__(self):
        self.item_file.close()
        self.rela_file.close()

    def start_requests(self):
        return srs.start_requests(self)
    
    def parse(self, response):
        if response.status in self.handle_httpstatus_list:
            srs.handle_error(self, response)
        else:
            self.error_time = 0
            srs.do_item_parse(self, response)
        srs.get_next_item(self)
        yield srs.yield_request(self)

