#!/usr/bin/env python

from ..util.html import get_content, url_info
from ..util.match import match1
from ..extractor import VideoExtractor

import json
import re

class Ku6(VideoExtractor):
    name = "酷6 (Ku6)"

    def prepare(self):
        assert self.url or self.vid
        if self.url and not self.vid:
            self.vid = match1(self.url, 'http://v.ku6.com/special/show_\d+/(.*)\.html',
            'http://v.ku6.com/show/(.*)\.html',
            'http://my.ku6.com/watch\?.*v=(.*).*')

        data = json.loads(get_content('http://v.ku6.com/fetchVideo4Player/%s.html' % self.vid))['data']
        self.title = data['t']
        f = data['f']


        urls = f.split(',')
        ext = re.sub(r'.*\.', '', urls[0])
        assert ext in ('flv', 'mp4', 'f4v'), ext
        ext = {'f4v': 'flv'}.get(ext, ext)
        size = 0
        for url in urls:
            _, _, temp = url_info(url)
            size += temp

        self.streams['current'] = {'container': ext, 'src': urls, 'size' : size}
        self.stream_types.append('current')

site = Ku6()
