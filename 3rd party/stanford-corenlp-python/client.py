# coding=utf-8
import json
from jsonrpc import ServerProxy, JsonRpc20, TransportTcpIp
from pprint import pprint
from wiki_parser import *
from entities import *

lemma_key = 'Lemma'

dependencies = ['nsubj', 'rep', 'dobj']
# modifiers = ['aux', u'animal', u'has']
#                                    [u'cop', u'animal', u'been'],
#                                    [u'det', u'animal', u'the'],
#                                    [u'amod',
sent_key = 'sentences'
deps_key = 'dependencies'
words_key = 'words'
concepts = ['dog']
candidates = []


class StanfordNLP:
    def __init__(self):
        # print 0
        self.server = ServerProxy(JsonRpc20(),
                                  TransportTcpIp(addr=("127.0.0.1", 8080)))

    def parse(self, text):
        # print self.server.parse(text)
        return json.loads(self.server.parse(text))

def build_statement(sent, main_dep):
    """

    :param sent:
    :param main_dep:
    :return:
    """
    stat = Statement()
    stat.left = Concept(main_dep[2])
    vp = main_dep[1]
    #searching for Lemma form of linked verb
    for word in sent[sent_key][0][words_key]:
        if word[0] in [main_dep[1]]:
            if word[1]['PartOfSpeech'][0] == 'V':
                stat.v = word[1][lemma_key]
            if word[1]['PartOfSpeech'][0] == 'N':
                stat.right.body = word[1][lemma_key]
                stat.v = 'is a'
            break
    #searching for right part of statement
    right_part = stat.right
    for dep in sent[sent_key][0][deps_key]:
        if dep[0] == 'dobj':
            if dep[1] in [main_dep[1]]:
                right_part.body = dep[2]
            break
    #search for right modifiers
    for dep in sent[sent_key][0][deps_key]:
        if dep[0] == 'amod':
            if dep[1] == right_part.body:
                right_part.modifiers.append(dep[2])
    stat.right = right_part
    print bcolors.OKGREEN + stat.__str__()
    # pprint(sent)



    return

def analyze_deps(result):
    # print result[sent_key][0][deps_key]
    # print result[sent_key][0][deps_key]
    try:
        for dep in result[sent_key][0][deps_key]:
            if dep[0] == 'nsubj':
                if concepts.__contains__(dep[2]):
                    build_statement(result, dep)
    except:
        print '\033[91m' + 'error during analyzing in sentence'
        print result

def process_sentence(text):
    global result, Tree, tree
    result = nlp.parse(text)
    analyze_deps(result)
    # pprint(result)
    from nltk.tree import Tree

    # tree = Tree.parse(result['sentences'][0]['parsetree'])
    # tree.draw()
    # tree.__contains__()




if __name__ == '__main__':
    nlp = StanfordNLP()
    text = get_data(concepts)
    s = ''
    for sentence in text:
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

