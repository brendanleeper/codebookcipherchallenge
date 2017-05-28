from collections import Counter, OrderedDict as odict
import re
from itertools import dropwhile
import numpy as np
from random import randint
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly.graph_objs as go

# Monoalphabetic Cipher with Homophones
ciphertext  = "IXDVMUFXLFEEFXSOQXYQVXSQTUIXWF*FMXYQVFJ*FXEFQUQXJFPTUFXMX*ISSFLQTUQXMXRPQEUMXUMTUIXYFSSFI*MXKFJF*FMXLQXTIEUVFXEQTEFXSOQXLQ*XVFWMTQTUQXTITXKIJ*FMUQXTQJMVX*QEYQVFQTHMXLFVQUVIXM*XEI*XLQ*XWITLIXEQTHGXJQTUQXSITEFLQVGUQX*GXKIEUVGXEQWQTHGXDGUFXTITXDIEUQXGXKFKQVXSIWQXAVPUFXWGXYQVXEQJPFVXKFVUPUQXQXSGTIESQTHGX*FXWFQFXSIWYGJTFXDQSFIXEFXGJPUFXSITXRPQEUGXIVGHFITXYFSSFI*CXC*XSCWWFTIXSOQXCXYQTCXYIESFCX*FXCKVQFXVFUQTPUFXQXKI*UCXTIEUVCXYIYYCXTQ*XWCUUFTIXLQFXVQWFXDCSQWWIXC*FXC*XDI**QXKI*IXEQWYVQXCSRPFEUCTLIXLC*X*CUIXWCTSFTIXUPUUQX*QXEUQ**QXJFCXLQX*C*UVIXYI*IXKQLQCX*CXTIUUQXQX*XTIEUVIXUCTUIXACEEIXSOQXTITXEPVJQCXDPIVXLQ*XWCVFTXEPI*IXSFTRPQXKI*UQXVCSSQEIXQXUCTUIXSCEEIX*IX*PWQXQVZXLFXEIUUIXLZX*ZX*PTZXYIFXSOQXTUVZUFXQVZKZWXTQX*Z*UIXYZEEIRPZTLIXTZYYZVKQXPTZXWITUZJTZXAVPTZXYQVX*ZXLFEUZTHZXQXYZVKQWFXZ*UZXUZTUIXRPZTUIXKQLPUZXTITXZKQZXZ*SPTZXTIFXSFXZ**QJVNWWIXQXUIEUIXUIVTIXFTXYFNTUIXSOQXLQX*NXTIKNXUQVVNXPTXUPVAIXTNSRPQXQXYQVSIEEQXLQ*X*QJTIXF*XYVFWIXSNTUIXUVQXKI*UQXF*XDQXJFVBVXSITXUPUUQX*BSRPQXBX*BXRPBVUBX*QKBVX*BXYIYYBXFTXEPEIXQX*BXYVIVBXFVQXFTXJFPXSIWB*UVPFXYFBSRPQFTDFTXSOQX*XWBVXDPXEIYVBXTIFXVFSOFPEIXX*BXYBVI*BXFTXSILFSQXQXQRPBUIV"

#ciphertext = "BT JPX RMLX PCUV AMLX ICVJP IBTWXVR CI M LMT'R PMTN, MTN YVCJX CDXV MWMBTRJ JPX AMTNGXRJBAH UQCT JPX QGMRJXV CI JPX YMGG CI JPX HBTW'R QMGMAX; MTN JPX HBTW RMY JPX QMVJ CI JPX PMTN JPMJ YVCJX. JPXT JPX HBTW'R ACUTJXTMTAX YMR APMTWXN, MTN PBR JPCUWPJR JVCUFGXN PBL, RC JPMJ JPX SCBTJR CI PBR GCBTR YXVX GCCRXN, MTN PBR HTXXR RLCJX CTX MWMBTRJ MTCJPXV. JPX HBTW AVBXN MGCUN JC FVBTW BT JPX MRJVCGCWXVR, JPX APMGNXMTR, MTN JPX RCCJPRMEXVR. MTN JPX HBTW RQMHX, MTN RMBN JC JPX YBRX LXT CI FMFEGCT, YPCRCXDXV RPMGG VXMN JPBR YVBJBTW, MTN RPCY LX JPX BTJXVQVXJMJBCT JPXVXCI, RPMGG FX AGCJPXN YBJP RAM"
#ciphertext = re.sub("[^a-zA-Z]+", "", ciphertext)

digrams = ['TH', 'HE', 'IN', 'ER', 'AN', 'RE', 'ED', 'ON', 'ES', 'ST', 'EN', 'AT',
           'TO', 'NT', 'HA', 'ND', 'OU', 'EA', 'NG', 'AS', 'OR', 'TI', 'IS', 'ET',
           'IT,' 'AR', 'TE', 'SE', 'HI', 'OF']

trigrams = ['THE', 'ING', 'AND', 'HER', 'ERE', 'ENT', 'THA', 'NTH', 'WAS', 'ETH', 'FOR', 'DTH']

common_repeats = ["SS", "EE", "TT", "FF", "LL", "MM", "OO"]

# english digram frequency map
E = [[1,32,39,15,0,10,18,0,16,0,10,77,18,172,2,31,1,101,67,124,12,24,7,0,27,1],
[8,0,0,0,58,0,0,0,6,2,0,21,1,0,11,0,0,6,5,0,25,0,0,0,19,0],
[44,0,12,0,55,1,0,46,15,0,8,16,0,0,59,1,0,7,1,38,16,0,1,0,0,0],
[45,18,4,10,39,12,2,3,57,1,0,7,9,5,37,7,1,10,32,39,8,4,9,0,6,0],
[131,11,64,107,39,23,20,15,40,1,2,46,43,120,46,32,14,154,145,80,7,16,41,17,17,0],
[21,2,9,1,25,14,1,6,21,1,0,10,3,2,38,3,0,4,8,42,11,1,4,0,1,0],
[11,2,1,1,32,3,1,16,10,0,0,4,1,3,23,1,0,21,7,13,8,0,2,0,1,0],
[84,1,2,1,251,2,0,5,72,0,0,3,1,2,46,1,0,8,3,22,2,0,7,0,1,0],
[18,7,55,16,37,27,10,0,0,0,8,39,32,169,63,3,0,21,106,88,0,14,1,1,0,4],
[0,0,0,0,2,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,4,0,0,0,0,0],
[0,0,0,0,28,0,0,0,8,0,0,0,0,3,3,0,0,0,2,1,0,0,3,0,3,0],
[34,7,8,28,72,5,1,0,57,1,3,55,4,1,28,2,2,2,12,19,8,2,5,0,47,0],
[56,9,1,2,48,0,0,1,26,0,0,0,5,3,28,16,0,0,6,6,13,0,2,0,3,0],
[54,7,31,118,64,8,75,9,37,3,3,10,7,9,65,7,0,5,51,110,12,4,15,1,14,0],
[9,18,18,16,3,94,3,3,13,0,5,17,44,145,23,29,0,113,37,53,96,13,36,0,4,2],
[21,1,0,0,40,0,0,7,8,0,0,29,0,0,28,26,0,42,3,14,7,0,1,0,2,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,20,0,0,0,0,0],
[57,4,14,16,148,6,6,3,77,1,11,12,15,12,54,8,0,18,39,63,6,5,10,0,17,0],
[75,13,21,6,84,13,6,30,42,0,2,6,14,19,71,24,2,6,41,121,30,2,27,0,4,0],
[56,14,6,9,94,5,1,315,128,0,0,12,14,8,111,8,0,30,32,53,22,4,16,0,21,0],
[18,5,17,11,11,1,12,2,5,0,0,28,9,33,2,17,0,49,42,45,0,0,0,1,1,1],
[15,0,0,0,53,0,0,0,19,0,0,0,0,0,6,0,0,0,0,0,0,0,0,0,0,0],
[32,0,3,4,30,1,0,48,37,0,0,4,1,10,17,2,0,1,3,6,1,1,2,0,0,0],
[3,0,5,0,1,0,0,0,4,0,0,0,0,0,1,4,0,0,0,1,1,0,0,0,0,0],
[11,11,10,4,12,3,5,5,18,0,0,6,4,3,28,7,0,5,17,21,1,3,14,0,0,0],
[0,0,0,0,5,0,0,0,2,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1]]

E = np.array(E)

abc = "abcdefghijklmnopqrstuvwxyz".upper()

mostcommon = "etaoinshrdlcumwfgypbvkjxqz".upper()

def getalphabet(text):
    return list(Counter(text).keys())

def stringtokey(a,b):
    return list(zip(a,b))

def dfm(text):
    # restrict to regular alphabet for now
    alphabet = getalphabet(abc)
    alphabet.sort()
    result = np.zeros((len(alphabet),len(alphabet)), dtype=np.int64)
    indexmap = dict(zip(alphabet,xrange(len(alphabet))))
    for i, character in enumerate(text):
        if i < len(text)-1 and character in indexmap and text[i+1] in indexmap:
            result[indexmap[character]][indexmap[text[i+1]]] += 1
    return result,indexmap

def d(X,Y):
    assert X.shape == Y.shape
    ilen = X.shape[0]
    jlen = X.shape[1]
    out = 0

    for i in xrange(ilen):
        for j in xrange(jlen):
            out += abs(X[i][j] - Y[i][j])
    return out

def getscore(E,C,K):
    return d(dfm(decode(C,K)),E)

def hillclimb(E, C, K):
    P = decode(C,K)
    D = dfm(P)
    Dd = np.copy(D)
    score = d(D,E)
    #score = np.linalg.norm(Dd-E)
    print "starting score %s" % score
    for i in xrange(len(K)-1):
        for j in xrange(len(K)-i):
            #swap rows j and j+i
            temp = np.copy(Dd[j,:])
            Dd[j,:] = np.copy(Dd[j+i,:])
            Dd[j+i,:] = temp
            #swap cols j and j+i
            temp = np.copy(Dd[:,j])
            Dd[:,j] = np.copy(Dd[:,j+i])
            Dd[:,j+i] = temp
            if d(Dd,E) < score:
                D = Dd
                temp = K[j][1]
                K[j] = (K[j][0],K[j+i][1])
                K[j+i] = (K[j+i][0],temp)
                score = d(Dd,E)
    return K, score

def hillclimb2(E,C,K):
    P = decode(C,K)
    D = dfm(P)
    score = d(D,E)
    Kk = K
    i = randint(0,len(K)-1)
    j = randint(0,len(K)-1)
    temp = Kk[j][1]
    Kk[j] = (Kk[j][0],Kk[i][1])
    Kk[i] = (Kk[i][0],temp)
    #print "old: %s, new: %s" % (score, d(dfm(decode(C,K)),E))
    return (Kk,getscore(E,C,K))

def decode(C, key):
    for k in key:
        C = C.replace(k[0], k[1])
    return C
#hillclimb(ciphertext)
#P = dfm(ciphertext)
#print d(P,E)
#K = stringtokey([x[0] for x in Counter(list(ciphertext)).most_common()], mostcommon)
#score = getscore(E,ciphertext,K)
'''
for i in xrange(10000):
    newkey,newscore = hillclimb2(E, ciphertext, K)
    if newscore < score:
        score = newscore
        K = newkey

key = []
D,indexmap = dfm(ciphertext)
invmap = dict((v, k) for k, v in indexmap.iteritems())
n = 0
for row in D:
    lowest = 99999999999
    lowestletter = ""
    lowestindex = -1
    for i in xrange(D.shape[0]):
        s = np.linalg.norm(E[i]-row)
        if s < lowest:
            lowest = s
            lowestletter = invmap[i]
            lowestindex = i
        #print "%s: %s" % (invmap[i], np.linalg.norm(E[i]-row))
    print "best match for %s: %s" % (invmap[n], lowestletter)
    #print row
    #print E[lowestindex]
    n += 1
'''
def countletters(text, graph=False):
    letters = list(text)
    lettercount = Counter(letters)
    x = []
    values = []
    print len(text)
    for k, v in lettercount.most_common():
        x.append(k)
        values.append(float(v)/len(text)*100.0)
    print x
    print values
    data = [go.Bar(x=x,y=values)]
    if graph:
        plot(data, filename='countletters.html', auto_open=False)

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
    for key, value in sorted(count.iteritems(), key=lambda (k,v): (v,k)):
        x.append(key)
        y.append(value)
    x.reverse()
    y.reverse()
    data = [go.Bar(x=x,y=y)]
    if graph:
        plot(data, filename='repeats.html', auto_open=False)

def digrams(text, graph=False, n=2):
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
        if value > 1:
            x.append(key)
            y.append(value)
    x.reverse()
    y.reverse()
    data = [go.Bar(x=x,y=y)]
    if graph:
        plot(data, filename='digrams-%s.html' % n, auto_open=False)

# space cannot be: U, E, S, Y, W, *, X, V?
# XX looks like space but it gets repeated
# maybe just to throw me off?
# other possibility is that space is many letters
# but X is still far too heavily weighted in that case
eliminated = "uesyw*xv".upper()
potentials = list(set(abc) - set(eliminated))
potentials.sort()
#print potentials
key = []
key.append(('X',' '))
key.append(('N','%'))
key.append(('G','%'))
key.append(('M','%'))
key.append(('Z','%'))
key.append(('B','%'))
key.append(('C','%'))
# these letters are individually super sparse
# they also don't digram in any meaningful ways
# together they're the most common (besides X)
#ciphertext = decode(ciphertext,key)
#countletters(ciphertext, True)
key.append(('%','a'))
key.append(('I', 'o'))
key.append(('Q', 'e'))
key.append(('D', 'f'))
key.append(('V', 'r'))
key.append(('F', 'i'))
key.append(('Y', 'p'))
key.append(('S', 'c'))
key.append(('O', 'h'))
key.append(('U', 't'))
key.append(('E', 's'))
key.append(('L', 'd'))
key.append(('T', 'n'))
key.append(('*', 'l'))
key.append(('W', 'm'))
key.append(('J', 'g'))
key.append(('P', 'u'))
key.append(('K', 'v'))
key.append(('A', 'b'))
key.append(('H', 'z'))
key.append(('R', 'q'))
# not even in english???
# it's dante's inferno: http://www.parafrasando.it/DANTE/Inferno_Canto_XXVI_Ulisse.html
#trace1 = go.Bar(x=list(abc),y=D[25])
#trace2 = go.Bar(x=list(abc),y=E[25])
#data = [trace1, trace2]
ciphertext = decode(ciphertext,key)
print ciphertext
#countletters(ciphertext,True)
repeats(ciphertext, True)
digrams(ciphertext, True, 1)
digrams(ciphertext, True, 2)
digrams(ciphertext, True, 3)
