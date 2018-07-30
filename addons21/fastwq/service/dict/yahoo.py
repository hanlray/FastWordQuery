# -*- coding:utf-8 -*-
import os
from ..base import *

yahoo_download_mp3 = True


@register([u'雅虎奇摩字典', u'Yahoo-Dict'])
class Yahoo_Dict(WebService):

    def __init__(self):
        super(Yahoo_Dict, self).__init__()

    def _get_content(self):
        url = u"https://tw.dictionary.search.yahoo.com/search?p={}".format(
            self.quote_word)
        html = self.get_response(url, timeout=10)
        soup = parse_html(html)
        result = {
            'phon': '',
            'def': '',
            'audio_url': '',
            'detail': '',
        }

        # 基本
        element = soup.find('div', class_='dd cardDesign dictionaryWordCard sys_dict_word_card')
        if element:
            # 音标
            tag = element.find('div', class_='compList ml-25 d-ib')
            if tag:
                result['phon'] = tag.get_text()

            # 发音
            result['audio_url'] = u'https://s.yimg.com/bg/dict/dreye/live/f/{}.mp3'.format(
                self.word)

            # 词性及中文解释
            tag = element.find('div', class_='compList mb-25 ml-25 p-rel')
            if tag:
                result['def'] = u'<div class="dd cardDesign">' + \
                    str(tag.find('ul')) + u'</div>'

        # 释义
        tag = soup.find('div', class_='grp grp-tab-content-explanation tabsContent tab-content-explanation tabActived')
        if tag:
            result['detail'] = u'<div class="dd cardDesign">' + \
                str(tag.find('ul')) + u'</div>'
        

        return self.cache_this(result)

    def _get_field(self, key, default=u''):
        return self.cache_result(key) if self.cached(key) else self._get_content().get(key, default)

    @with_styles(need_wrap_css=True, cssfile='_yahoo.css')
    def _css(self, val):
        return val

    @export(u'音标')
    def fld_pinyin(self):
        return self._get_field('phon')

    @export(u'发音')
    def fld_pron(self):
        audio_url = self._get_field('audio_url')
        if yahoo_download_mp3 and audio_url:
            filename = u'_yahoo_dict_{}_.mp3'.format(self.word)
            filename = get_hex_name(self.unique.lower(), filename, 'mp3')
            if os.path.exists(filename) or self.download(audio_url, filename, 5):
                return self.get_anki_label(filename, 'audio')

        return ''

    @export(u'中文释义')
    def fld_basic(self):
        val = self._get_field('def')
        if val is None or val == '':
            return ''
        return self._css(val)

    @export(u'详细释义')
    def fld_detail(self):
        val = self._get_field('detail')
        if val is None or val == '':
            return ''
        return self._css(val)
