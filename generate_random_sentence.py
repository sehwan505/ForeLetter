import bisect
import itertools
import random
from datetime import datetime

import nltk
from konlpy.corpus import kolaw
from eunjeon import Mecab # MeCab tends to reserve the original form of morphemes


def generate_sentence(cfdist, word, num=15):
    sentence = []

    # Generate words until we meet a period
    while word!='.':
        sentence.append(word)

        # Generate the next word based on probability
        choices, weights = zip(*cfdist[word].items())
        cumdist = list(itertools.accumulate(weights))
        x = random.random() * cumdist[-1]
        word = choices[bisect.bisect(cumdist, x)]

    return ' '.join(sentence)


def calc_cfd(doc):
    # Calculate conditional frequency distribution of bigrams
    words = [w for w, t in Mecab().pos(doc)]
    bigrams = nltk.bigrams(words)
    return nltk.ConditionalFreqDist(bigrams)


if __name__=='__main__':
    nsents = 5 # Number of sentences
    initstr = u'국민' # Try replacing with u'국가', u'대통령', etc

    doc = kolaw.open('constitution.txt').read()
    cfd = calc_cfd(doc)

    txtfile = open("test.txt","a",encoding="utf-8")
    txtfile.write(str(datetime.now()))
    txtfile.write('\n')

    for i in range(nsents):
        randsentence = generate_sentence(cfd,initstr)

        txtfile.write(randsentence)
        txtfile.write('\n')
        print('%d. %s' % (i, randsentence))
    txtfile.close()