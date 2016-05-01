#!/usr/bin/env python
from ..util.html import get_content
from ..util.match import match1
from ..extractor import VideoExtractor
import urllib.parse
import json

class HuomaoTv(VideoExtractor):
    name = '火猫 (Huomao)'

    supported_stream_types = ['TD', 'HD', 'SD', 'BD' ]

    stream_2_profile = {'TD': '超清', 'HD': '高清', 'SD': '标清',  'BD':"unknown" }

    live_base = "http://www.huomaotv.cn/swf/live_data"

    def prepare(self):
        assert self.url

        html = get_content(self.url)
        self.title = match1(html, '<title>([^<]+)')

        video_name = match1(html, 'video_name = \'([^\']+)')
        params = { 'streamtype':'live',
                   'VideoIDS': video_name,
                   'cdns' : '1'
                }
        form = urllib.parse.urlencode(params)
        content = get_content(self.live_base,data=bytes(form, 'utf-8'),charset = 'utf-8')
        stream_data = json.loads(content)
        if stream_data["roomStatus"] == "1":
            for stream in stream_data["streamList"]:
                if stream['default'] == 1:
                    defstream = stream['list']
        else:
           from ..util import log
           log.e("The live stream is not online! ")
           exit(1)
        for stream in defstream:
            self.stream_types.append(stream['type'])
            self.streams[stream['type']] = {'container': 'flv', 'video_profile': self.stream_2_profile[stream['type']], 'src' : [stream['url']], 'size': float('inf')}

        self.stream_types = sorted(self.stream_types, key = self.supported_stream_types.index)

site = HuomaoTv()
