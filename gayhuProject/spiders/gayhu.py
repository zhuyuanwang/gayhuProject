# -*- coding: utf-8 -*-
import scrapy
import time
import re
import os
from ..settings import DEFAULT_REQUEST_HEADERS,COOKIES
from urllib.request import urlretrieve


class GayhuSpider(scrapy.Spider):
    name = 'gayhu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']

    def start_requests(self):
        # 时间 2019年7月4日16:49:19
        # 问题id，可手动添加
        questionid = '22132862'
        # 某必备参数，可直接从网页获取
        include = 'data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_labeled%2Cis_recognized%2Cpaid_info%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%2A%5D.topics'
        # 页码偏移量根据该问题的回答次数设置，这里为了方便手动设置
        for offset in range(0, 180, 5):
            time.sleep(2)
            url = 'https://www.zhihu.com/api/v4/questions/{}/answers?include={}&limit=5&offset={}&platform=desktop&sort_by=default'.format(questionid, include, offset)
            yield scrapy.Request(url=url, headers=DEFAULT_REQUEST_HEADERS, cookies=COOKIES, callback=self.parse_info,meta={'questionid':questionid})

    def parse_info(self, response):

        # 使用questionid做为图片目录名
        questionid = response.meta['questionid']
        picurllist = []
        # 使用正则匹配图片链接
        picurl = re.findall('data-original=(.*?)r.jpg', response.text)
        for pic in picurl:
            picurl = pic.split('"')[-1].replace('\\u002F', '/')
            realpic = picurl + 'r.jpg'
            if realpic not in picurllist:
                picurllist.append(realpic)

        con = 0
        for pic_url in picurllist:
            time.sleep(2)
            con += 1
            if not os.path.exists(questionid):
                os.makedirs(questionid)
            # 图片名由图片链接截取命名
            pic_name = os.path.basename(pic_url)
            print('正在下载：{},第{}张'.format(pic_name, con))
            urlretrieve(pic_url, './{}/{}'.format(questionid,pic_name))
