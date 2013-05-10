# coding=utf-8
from wikipedia import *
from wiki2plain import *

lang = 'en'
wiki = Wikipedia(lang)


def get_data(articles):
    ret_list = []

    for article in articles:
        try:
            raw = wiki.article(article)
        except:
            raw = None

        if raw:
            wiki2plain = Wiki2Plain(raw)
            content = wiki2plain.text
            # print content
            res = re.findall('[A-Z][^\.=;कš\*]*' + article.lower() + '[^\.;कš\*]*', content)
            ret_list.append(res)

    return ret_list