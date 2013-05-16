# coding=utf-8
import json
import os
from jsonrpc import ServerProxy, JsonRpc20, TransportTcpIp
from pprint import pprint
from wiki_parser import *
from entities import *
from clustering_manager import *

lemma_key = 'Lemma'
statements_output = 'retreived_statements.txt'
dependencies = ['nsubj', 'prep', 'dobj']
# modifiers = ['aux', u'animal', u'has']
#                                    [u'cop', u'animal', u'been'],
#                                    [u'det', u'animal', u'the'],
#                                    [u'amod',
sent_key = 'sentences'
deps_key = 'dependencies'
words_key = 'words'
# 'mouse', 'mammal', 'amniote',
concepts = ['dog', 'mammal', 'tetrapod']
candidates = []
statements = []


class StanfordNLP:
    def __init__(self):
        # print 0
        self.server = ServerProxy(JsonRpc20(),
                                  TransportTcpIp(addr=("127.0.0.1", 8080)))

    def parse(self, text):
        # print self.server.parse(text)
        return json.loads(self.server.parse(text))


def build_statement(sent, main_dep, word):
    """
    :param sent:
    :param main_dep:
    :return:
    """
    ret_list = []
    stat = Statement()
    stat.left = Concept(word[1][lemma_key])
    vp = main_dep[1]
    #searching for Lemma form of linked verb
    for word in sent[sent_key][0][words_key]:
        if word[0] in [main_dep[1]]:
            if word[1]['PartOfSpeech'][0] == 'V':
                stat.v = word[1][lemma_key]
            if word[1]['PartOfSpeech'][0] == 'N':
                stat.right.body = word[1][lemma_key]
                stat.v = 'is_a'
            if word[1]['PartOfSpeech'][0] == 'J':
                stat.right.body = word[1][lemma_key]
                stat.v = 'is_a'
            break
    #searching for right part of statement
    # right_part = stat.right

    #search for right modifiers
    if not stat.right.body == '':
        for dep in sent[sent_key][0][deps_key]:
            if dep[0] == 'amod':
                if dep[1] == stat.right.body:
                    stat.right.modifiers.append(dep[2])
        print bcolors.OKGREEN + stat.__str__()
        ret_list.append(stat)
        return ret_list

    for dep in sent[sent_key][0][deps_key]:
        sta_cond = Statement()
        sta_cond.left = Concept(stat.left.body)
        sta_cond.v = stat.v
        prep = ''
        right_part = Concept('')
        if dep[0] == 'dobj':
            if dep[1] in [main_dep[1]]:
                right_part.body = dep[2]
        if 'prep' in dep[0]:
            if dep[1] in [main_dep[1]]:
                right_part.body = dep[2]
                tmp = dep[0].split('_')
                prep = '_' + tmp[1]

        #search for right modifiers
        if not right_part.body == '':
            for dep in sent[sent_key][0][deps_key]:
                if dep[0] == 'amod':
                    if dep[1] == right_part.body:
                        right_part.modifiers.append(dep[2])
            sta_cond.right = right_part

            sta_cond.v += prep
            print bcolors.OKGREEN + sta_cond.__str__()
            ret_list.append(sta_cond)

    # pprint(sent)
    return ret_list

def analyze_deps(result):
    # print result[sent_key][0][deps_key]
    # print result[sent_key][0][deps_key]
    try:
        for dep in result[sent_key][0][deps_key]:
            if 'nsubj' in dep[0]:
                for wrd in result[sent_key][0][words_key]:
                    if wrd[1][lemma_key] in concepts:
                        if dep[2].lower() == wrd[0].lower():
                            s_list = build_statement(result, dep, wrd)
                            for s in s_list:
                                if s.right.body != '':
                                    statements.append(s)
    except:
        print '\033[91m' + 'error during analyzing in sentence'
        print result

    return statements

def process_sentence(text):
    global result, Tree, tree
    result = nlp.parse(text)
    ret_list = analyze_deps(result)
    pprint(result)
    from nltk.tree import Tree

    # tree = Tree.parse(result['sentences'][0]['parsetree'])
    # tree.draw()
    # tree.__contains__()


def store_statements():
    for s in statements:
        f.write(s.__str__())
        f.write('\n')
    return


def read_from_file():
    f = open(statements_output, 'r')
    ret_list = []
    lines = f.readlines()
    for line in lines:
        parts = line.split(' ')
        s = Statement()
        s.left.body = parts[0]
        s.v = parts[1]
        for i in range(2, len(parts)-1):
            s.right.modifiers.append(parts[i])
        s.right.body = parts[len(parts)-1].split('\n')[0]
        ret_list.append(s)
        # print s
    return ret_list


if __name__ == '__main__':
    nlp = StanfordNLP()
    articles = get_data(concepts)
    # s = 'The first tetrapods were cool aquatic and fed primarily on fish'
    # process_sentence(s)
    if not os.path.isfile(statements_output):
        for article in articles:
            for sentence in article:
                try:
                    print bcolors.ENDC + sentence
                    s = sentence
                    if len(sentence) < 400:
                        process_sentence(sentence)
                        # break
                        # pprint(tree)
                        # tree.draw()
                except:
                    print bcolors.FAIL + 'parsing error in sentence ' + s
        f = open(statements_output, 'w+')
        store_statements()
    else:
        statements = read_from_file()
    synset_man = SynsetRetreiver()
    synset_man.find_synsets(statements)

