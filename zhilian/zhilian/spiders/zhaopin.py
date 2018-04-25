# -*- coding: utf-8 -*-
import re
import time

import scrapy
# from tqdm import tqdm
from scrapy import Request
from zhilian.items import ZhilianItem


class ZhaopinSpider(scrapy.Spider):
    name = 'zhaopin'
    allowed_domains = ['www.zhaopin.com']
    start_urls = ['http://www.zhaopin.com/']

    query = {
        'jl': ' 上海',
        'kw': ' python工程师',
        'sm': 0,
        'p': 1
    }

    search_url = 'http://sou.zhaopin.com/jobs/searchresult.ashx?jl={jl}&kw={kw}&sm={sm}&p={p}'  # 从网站首页输入工作信息后跳转的第一个页面也是第一个爬取页面

    def start_requests(self):
        yield Request(url=self.search_url.format(**self.query), callback=self.index_parse)

    def index_parse(self, response):
        detail_urls = re.findall(r'<td class="zwmc".*?href="(.*?)"', response.text, re.S)
        # for detail_url in tqdm(detail_urls):
        for detail_url in detail_urls:
            item = ZhilianItem()
            item['detail_url'] = detail_url
            yield Request(url=item['detail_url'], meta={'item': item}, callback=self.detail_parse, dont_filter=True)
            if response.css('.newlist_wrap.fl > div.pagesDown > ul > li.pagesDown-pos > a::attr(href)').extract():
                self.query['p'] += 1
                yield Request(url=self.search_url.format(**self.query), callback=self.index_parse)

    def detail_parse(self, response):
        item = response.meta['item']
        job = response.css('.top-fixed-box .fixed-inner-box .fl h1::text').extract_first()
        company = response.css('.top-fixed-box .fixed-inner-box .fl h2 a::text').extract_first()
        salary = response.css(
            '.terminalpage.clearfix .terminalpage-left > ul > li:nth-child(1) > strong::text').extract_first()
        educational = response.css(
            '.terminalpage.clearfix .terminalpage-left > ul > li:nth-child(6) > strong::text').extract_first()
        experience = response.css(
            '.terminalpage.clearfix .terminalpage-left > ul > li:nth-child(5) > strong::text').extract_first()

        requirement = ''
        for terminalpage in response.css('.terminalpage-main .tab-cont-box .tab-inner-cont > p::text').extract():
            requirement += terminalpage.replace("\n", "").strip()
        pattern = re.compile(r'[一-龥]+')
        filterdata = re.findall(pattern, requirement)
        item['job'] = job
        item['company'] = company
        item['salary'] = salary
        item['educational'] = educational
        item['experience'] = experience
        item['requirement'] = ''.join(filterdata)
        # item['requirement'] = requirement

        yield item
