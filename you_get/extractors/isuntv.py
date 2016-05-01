#!/usr/bin/env python

from ..util.match import match1
from ..util.html import get_content, fake_headers
from ..extractor import VideoExtractor
import urllib.parse

class Isuntv(VideoExtractor):
    name = "阳光卫视 (SunTV)"

    API_URL = "http://www.isuntv.com/ajaxpro/SunTv.pro_vod_playcatemp4,App_Web_playcatemp4.ascx.9f08f04f.ashx"

    def prepare(self):
        assert self.url

        itemid = match1(self.url, r'http://www.isuntv.com/pro/ct(\d+).html')

        values = {"itemid" : itemid, "vodid": ""}
        data = str(values).replace("'", '"').encode('utf-8')

        header = fake_headers
        header['AjaxPro-Method'] = 'ToPlay'

        content = get_content(self.API_URL, data=data, headers = header)

        video_url = 'http://www.isuntv.com' + content.strip('"')

        html = get_content(self.url, charset = 'gbk')

        self.title = match1(html, '<title>([^<]+)').strip()  #get rid of \r\n s

        self.stream_types.append('current')
        self.streams['current'] = {'container': 'mp4', 'src': [video_url], 'size' : url_size(video_url)}


site = Isuntv()
