import json
import scrapy
import rela_single_spider as rss
''' 
    class for crawling repo list by user_star.txt 
    where store the relationship between user and repos they starred
    and store the result to file repo.txt
'''
class StarRepoSpider(scrapy.spiders.Spider):
    name = "star_repo"
    allowed_domains = ["github.com"]
    src_table = 'user_repo'
    src_key = ['repo']
    des_table = 'repo'
    des_key = ['full_name','id','private','name','fork','language','forks_count','stargazers_count','watchers_count','size','open_issues_count','pushed_at','created_at','updated_at']
    res_1key = ['owner']
    res_2key = ['login']
    des_2key = ['owner_login']
    des_val = {}
    cur_item = ''
    cur_item_ind = 0
    all_item = []
    base_url = "https://api.github.com/repos/"
    error_time = 0
    time_inter = rss.time_inter
    handle_httpstatus_list = rss.handle_httpstatus_list
    
    # monkey patching for scrapy.xlib.tx._newclient.HTTPClientParser.statusReceived
    def _monkey_patching_HTTPClientParser_statusReceived(self):
        from twisted.web._newclient import HTTPClientParser, ParseError
        old_sr = HTTPClientParser.statusReceived
        def statusReceived(self, status):
            try:
                return old_sr(self, status)
            except ParseError, e:
                if e.args[0] == 'wrong number of parts':
                    return old_sr(self, status + ' OK')
                raise
        statusReceived.__doc__ == old_sr.__doc__
        HTTPClientParser.statusReceived = statusReceived
    
    def __init__(self):
        self._monkey_patching_HTTPClientParser_statusReceived()
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

