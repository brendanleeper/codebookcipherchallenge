from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly.graph_objs as go
from collections import Counter
import re
from toolz import interleave

abc = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

vigeneresquare = []

def digrams(text, graph=False, n=2, c=1, counter=True):
    count = {}
    for i in xrange(len(text)-(n-1)):
        repeat = ""
        for j in xrange(n):
            repeat += text[i+j]
        if ' ' not in repeat:
            if repeat in count:
                count[repeat] += 1
            else:
                count[repeat] = 1
    x = []
    y = []
    for key, value in sorted(count.iteritems(), key=lambda (k,v): (v,k)):
        if value > c:
            x.append(key)
            y.append(value)
        else:
            del(count[key])
    x.reverse()
    y.reverse()
    data = [go.Bar(x=x,y=y)]
    if graph:
        plot(data, filename='digrams-%s.html' % n, auto_open=False)
    if counter:
        return Counter(count).most_common()
    else:
        return x

def repeats(text, graph=False):
    count = {}
    for i in xrange(len(text)-1):
        if text[i] == text[i+1]:
            repeat = text[i]+text[i]
            if repeat in count:
                count[repeat] += 1
            else:
                count[repeat] = 1
    x = []
    y = []
    out = {}
    for key, value in sorted(count.iteritems(), key=lambda (k,v): (v,k)):
        x.append(key)
        y.append(value)
        out[key] = value
    x.reverse()
    y.reverse()
    data = [go.Bar(x=x,y=y)]
    if graph:
        plot(data, filename='repeats.html', auto_open=False)
    return Counter(count).most_common()

def digramdist(text, digram):
    matches = []
    for m in re.finditer(digram, text):
         #print(digram, m.start(), m.end())
         matches.append(m.start())
    return matches

def factors(n):
    return set(reduce(list.__add__, ([i, n//i] for i in range(1, int(n**0.5) + 1) if n % i == 0)))

def mostcommondigramfactors(text, trigrams):
    indices = []
    allresults = []
    for t,_ in trigrams:
        i = digramdist(text, t)

        distances = []
        for m in xrange(len(i)-1):
            distances.append(i[m+1] - i[m])

        allfactors = []
        for d in distances:
            allfactors.append(factors(d))

        result = set(allfactors[0])
        for s in allfactors[1:]:
            result.intersection_update(s)
        allresults.append(list(result))

    flattened = [item for sublist in allresults for item in sublist]
    flattened = [item for item in flattened if item > 1]
    print flattened
    return Counter(flattened).most_common()

def offsetsplit(text, offset):
    i = 0
    result = []

    for n in xrange(offset):
        result.append("")

    for i,c in enumerate(text):
        result[i%5] += c

    return result

def offsetcombine(texts):
    return ''.join(interleave(texts))

def getalphabetposition(character, alphabet='ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
    return alphabet.upper().index(character.upper())

def getpositionletter(position):
    return '' + abc[position].lower()

def shiftalphabet(shift):
    out = ['' for x in range(1000)]
    orda = ord('A')
    for index, character in enumerate(abc):
        if(character != " "):
            out[index] = chr(((ord(character) - orda) + shift) % 26 + orda)
    out = ''.join(out)
    return out

for i in xrange(26):
    vigeneresquare.append(shiftalphabet(i))

def vigenerelookup(a, b, vigenere=vigeneresquare):
    ''' for guessing the key '''
    return vigenere[abs(getalphabetposition(a) - getalphabetposition(b))][0]

def guesskey(digrams=['IDGM'], commondigrams=['THEN']):
    keys = []
    for cd in commondigrams:
        for d in digrams:
            key = ''
            for i,c in enumerate(d):
                key += vigenerelookup(cd[i], c)
            print 'digram: %s, guess: %s, key: %s' % (d, cd, key)
            keys.append(key)
    return keys

def vdecode(letter, keychar, vigenere=vigeneresquare):
    if keychar == '_':
        return '#'
    return getpositionletter(getalphabetposition(letter, vigenere[getalphabetposition(keychar)])).lower()

def vigeneredecode(ciphertext, key):
    out = ''
    for i,c in enumerate(ciphertext):
        out += vdecode(c,key[i%len(key)])
    return out
