# -*- coding:utf-8 -*-
import random
import re

from bs4 import BeautifulSoup

from . import DefinitionLang
from ..base import *

VOICE_PATTERN = r'href="sound:\/\/([\w\/]+%s\/\w*\.mp3)"'
VOICE_PATTERN_WQ = r'<span class="%s"><a href="sound://([\w/]+\w*\.mp3)">(.*?)</span %s>'
MAPPINGS = [
    ['br', [re.compile(VOICE_PATTERN % r'breProns')]],
    ['us', [re.compile(VOICE_PATTERN % r'ameProns')]]
]
LANG_TO_REGEXPS = {lang: regexps for lang, regexps in MAPPINGS}

DEF_CN_PATTERN = re.compile(
    r'<span class="DEF LDOCE_switch_lang switch_siblings"> <span class="cn_txt">(\w+)</span></span>')

# u'E:\\BaiduYunDownload\\mdx\\L6mp3.mdx'
DICT_PATH = u'D:\\dict\\LDOCE5++ V 2-15\\LDOCE5++ V 2-15.mdx'


@register([u'本地词典-LDOCE5++', u'MDX-LDOCE5++'])
class Ldoce5plus(MdxService):

    def __init__(self):
        dict_path = DICT_PATH
        # if DICT_PATH is a path, stop auto detect
        if not dict_path:
            from ...service import service_manager, service_pool
            for clazz in service_manager.mdx_services:
                service = service_pool.get(clazz.__unique__)
                title = service.builder._title if service and service.support else u''
                service_pool.put(service)
                if title.startswith(u'LDOCE5++'):
                    dict_path = service.dict_path
                    break
        super(Ldoce5plus, self).__init__(dict_path)

    @property
    def title(self):
        return getattr(self, '__register_label__', self.unique)

    def _fld_voice(self, html, voice):
        """获取发音字段"""
        for regexp in LANG_TO_REGEXPS[voice]:
            match = regexp.search(html)
            if match:
                val = '/' + match.group(1)
                name = get_hex_name('mdx-'+self.unique.lower(), val, 'mp3')
                name = self.save_file(val, name)
                if name:
                    return self.get_anki_label(name, 'audio')
        return ''

    @export('BRE_PRON')
    def fld_voicebre(self):
        return self._fld_voice(self.get_html(), 'br')

    @export('AME_PRON')
    def fld_voiceame(self):
        return self._fld_voice(self.get_html(), 'us')

    @export('DEF_CN_1_part_1_sense_1_sentence')
    def fld_cn_111(self):
        return self._range_definition(DefinitionLang.CHN, 1, 1, 1)

    @export('DEF_CN_1_part_1_sense_1_sentence_audio')
    def fld_cn_111a(self):
        # sys.stdout.write(self.get_html())
        return self._range_definition(DefinitionLang.CHN, 1, 1, 1, True)

    @export('DEF_CN_1_part_1_sense_2_sentence')
    def fld_cn_112(self):
        return self._format_tab(self._range_definition(DefinitionLang.CHN, 1, 1, 2))

    @export('DEF_CN_1_part_1_sense_2_sentence_audio')
    def fld_cn_112a(self):
        # sys.stdout.write(self.get_html())
        return self._range_definition(DefinitionLang.CHN, 1, 1, 2, True)

    @export('DEF_CN_2_part_1_sense_2_sentence')
    def fld_cn_212(self):
        return self._css(self._format_tab(self._range_definition(DefinitionLang.CHN, 2, 1, 2)))

    @export('DEF_CN_2_part_1_sense_2_sentence_audio')
    def fld_cn_212a(self):
        return self._css(self._format_tab(self._range_definition(DefinitionLang.CHN, 2, 1, 2, True)))

    @export('DEF_EN_2_part_1_sense_2_sentence_audio')
    def fld_en_212a(self):
        return self._css(self._format_tab(self._range_definition(DefinitionLang.ENG, 2, 1, 2, True)))

    @export('DEF_EN_2_part_2_sense_2_sentence_audio')
    def fld_en_222a(self):
        return self._css(self._format_tab(self._range_definition(DefinitionLang.ENG, 2, 2, 2, True)))

    @staticmethod
    def _format_tab(def_result):
        parts = def_result['parts']
        result = '<div class="tabs">'
        for i, entry_key in enumerate(parts):
            result += '''
            <div class="tab">
                <input type="radio" id="{0}" name="tab-group-1"{2}>
                <label for="{0}">{0}</label>
                <div class="content">{1}</div>
            </div>
            '''.format(entry_key, parts[entry_key], ' checked' if i == 0 else '')
        result += '</div>'

        return result

    def _range_definition(self, lang, part_count, sense_count, sentence_count, with_audio=False):
        #sys.stdout.write(self.get_html())
        soup = BeautifulSoup(self.get_html(), 'html.parser')
        entries = soup.find_all("div", class_="dictentry")
        
        part_index = 0
        parts = {}
        result = {}
        files = []
        for entry in entries:
            if 'bussdict' in entry['class']:
                continue
        
            #head = entry.find('span', class_='frequent Head')
            part_elem = entry.select_one('.Head .lm5pp_POS')
            if part_elem:
                portrait = part_elem.select_one('.portrait')
                if portrait:
                    part = portrait.get_text()
                else:
                    part = part_elem.get_text()

                senses_text = '<ol>'
                senses = entry.find_all('div', class_='Sense')
                for j, sense in enumerate(senses):
                    if sense.select_one('.DEF') is None:
                        break

                    if lang == DefinitionLang.ENG:
                        sense_head = sense.select_one('.DEF').get_text()
                    elif lang == DefinitionLang.CHN:
                        sense_head = sense.select_one('.DEF .cn_txt').get_text()
                    elif lang == DefinitionLang.BILINGUAL:
                        sense_head = sense.select_one('.DEF').get_text() + sense.select_one('.DEF .cn_txt').get_text()

                    sentences = self._range_sentence(lang, sense, sentence_count, with_audio)
                    if isinstance(sentences, QueryResult):
                        files.extend(sentences['files'])
                        sentences = sentences['result']

                    senses_text += '<li>{0}{1}</li>'.format(sense_head, sentences)

                    if j == (sense_count - 1):
                        break

                parts[part] = senses_text + '</ol>'

                part_index += 1
                if part_index == part_count:
                    break
        # sys.stdout.write(str(result))
        result['parts'] = parts
        if len(files) > 0:
            result['files'] = files
        #print(result)
        return result

    def _range_sentence(self, lang, sense_elem, sentence_count, with_audio):
        if sentence_count <= 0:
            return ''

        result = '<ul>'
        files = []
        examples = sense_elem.find_all('div', class_="EXAMPLE", recursive=False)
        for i, example in enumerate(examples):
            english_elem = example.select_one('.english')
            if english_elem is None:
                break

            if lang == DefinitionLang.ENG:
                english_elem.select_one('.cn_txt').decompose()

            result += '<li>' + english_elem.get_text()
            if with_audio:
                speaker = example.select_one('.speaker')
                if speaker is None:
                    break

                audio_href = speaker['href']
                audio_path = audio_href.replace('sound:/', '')
                name = get_hex_name('mdx-' + self.unique.lower(), audio_path, 'mp3')
                name = self.save_file(audio_path, name)
                if name:
                    result += self.get_anki_label(name, 'audio')
                    files.append(name)
            result += '</li>'
            if i == (sentence_count - 1):
                break

        result += '</ul>'
        if len(files) > 0:
            return QueryResult(result=result, files=files)

        return result

    @with_styles(cssfile='_common.css')
    def _css(self, val):
        return val

    @export('All examples with audios')
    def fld_sentence_audio(self):
        return self._range_sentence_audio([i for i in range(0, 100)])

    @export('Random example with audio')
    def fld_random_sentence_audio(self):
        return self._range_sentence_audio()

    @export('First example with audio')
    def fld_first1_sentence_audio(self):
        return self._range_sentence_audio([0])

    @export('First 2 examples with audios')
    def fld_first2_sentence_audio(self):
        return self._range_sentence_audio([0, 1])

    def _fld_audio(self, audio):
        name = get_hex_name('mdx-'+self.unique.lower(), audio, 'mp3')
        name = self.save_file(audio, name)
        if name:
            return self.get_anki_label(name, 'audio')
        return ''

    def _range_sentence_audio(self, range_arr=None):
        m = re.findall(
            r'<div class="EXAMPLE">\s*.*>\s*.*<\/div>', self.get_html())
        if m:
            soup = parse_html(m[0])
            el_list = soup.findAll('div', {'class': 'EXAMPLE'})
            if el_list:
                maps = []
                for element in el_list:
                    i_str = ''
                    for content in element.contents:
                        i_str = i_str + str(content)
                    sound = re.search(
                        r'<a[^>]+?href=\"sound\:\/(.*?\.mp3)\".*<\/a>', i_str)
                    if sound:
                        maps.append([sound, i_str])
            my_str = ''
            range_arr = range_arr if range_arr else [
                random.randrange(0, len(maps) - 1, 1)]
            for i, e in enumerate(maps):
                if i in range_arr:
                    i_str = e[1]
                    sound = e[0]
                    mp3 = self._fld_audio(sound.groups()[0])
                    i_str = re.sub('<[^<]+?>', '', i_str)
                    i_str = re.sub('\xa0', '', i_str)
                    # i_str = re.sub(r'<a[^>]+?href=\"sound\:\/.*?\.mp3\".*<\/a>', '', i_str).strip()
                    # chinese text
                    # cn_text = re.search(r'<div class="cn_txt">(\s*\S*)<\/div><\/span>', i_str)
                    # cn_text_strip = " "
                    # if cn_text:
                    #     cn_text_strip = cn_text.groups()[0]
                    # i_str = re.sub(r'(<div class="cn_txt">\s*\S*<\/div>)<\/span>', '', i_str).strip()
                    # my_str = my_str + mp3 + ' ' + i_str  + cn_text_strip + '<br>'
                    my_str = my_str + mp3 + ' ' + i_str + '<br>'
            return my_str
        return ''
