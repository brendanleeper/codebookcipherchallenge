from usefulfunctions import *
from collections import Counter
f = open('stage4_cleaned.txt')

ciphertext = f.read()
#ciphertext = ciphertext.replace(' ', '')
#ciphertext.strip()
ciphertext = """
KQOWEFVJPUJUUNUKGLMEKJI
NMWUXFQMKJBGWRLFNFGHUDW
UUMBSVLPSNCMUEKQCTESWRE
EKOYSSIWCTUAXYOTAPXPLWP
NTCGOJBGFQHTDWXIZAYGFFN
SXCSEYNCTSSPNTUJNYTGGWZ
GRWUUNEJUUQEAPYMEKQHUID
UXFPGUYTSMTFFSHNUOCZGMR
UWEYTRGKMEEDCTVRECFBDJQ
CUSWVBPNLGOYLSKMTEFVJJT
WWMFMWPNMEMTMHRSPXFSSKF
FSTNUOCZGMDOEOYEEKCPJRG
PMURSKHFRSEIUEVGOYCWXIZ
AYGOSAANYDOEOYJLWUNHAME
BFELXYVLWNOJNSIOFRWUCCE
SWKVIDGMUCGOCRUWGNMAAFF
VNSIUDEKQHCEUCPFCMPVSUD
GAVEMNYMAMVLFMAOYFNTQCU
AFVFJNXKLNEIWCWODCCULWR
IFTWGMUSWOVMATNYBUHTCOC
WFYTNMGYTQMKBBNLGFBTWOJ
FTWGNTEJKNEEDCLDHWTVBUV
GFBIJGYYIDGMVRDGMPLSWGJ
LAGOEEKJOFEKNYNOLRIVRWV
UHEIWUURWGMUTJCDBNKGMBI
DGMEEYGUOTDGGQEUJYOTVGG
BRUJYS
"""

ciphertext = ciphertext.replace('\n', '')

#digrams(ciphertext, True, 1, 2)
#digrams(ciphertext, True, 2, 2)
trigrams = digrams(ciphertext, True, 3, 2, False)
#fourgrams = digrams(ciphertext, True, 4, 2)
#print fourgrams
# IDGM - 3 occurences = have?
#repeats(ciphertext, True)

#print digramdist(ciphertext, 'DGM')
# most common trigram and DG is most common bigram, assume its 'the'
# 350, 515, 520, 575

#print mostcommondigramfactors(ciphertext, trigrams)
# 5: 5, 3: 2, 15: 2
#print mostcommondigramfactors(ciphertext, fourgrams)
# 3: 1, 5: 1, 15: 1
# key is 5 characters long

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

# split the ciphertext into 5 ciphertexts based on their offset from 0
texts = offsetsplit(ciphertext, 5)
#for text in texts:
    #countletters(text, True)
returned = offsetcombine(texts)
# confirm we can return it back to a single string properly
assert returned == ciphertext
#texts[0] = texts[0].replace('D', 't')
#texts[1] = texts[1].replace('G', 'h')
#texts[2] = texts[2].replace('M', 'e')

#print ciphertext
#print combined
#print combined == ciphertext
#print interleaved

commondigrams = ['TH', 'HE', 'IN', 'ER', 'AN', 'RE', 'ED', 'ON', 'ES', 'ST', 'EN', 'AT',
           'TO', 'NT', 'HA', 'ND', 'OU', 'EA', 'NG', 'AS', 'OR', 'TI', 'IS', 'ET',
           'IT', 'AR', 'TE', 'SE', 'HI', 'OF']
commontrigrams = ['THE', 'ING', 'AND', 'HER', 'ERE', 'ENT', 'THA', 'NTH', 'WAS', 'ETH', 'FOR', 'DTH']
commonfourgrams = ['that', 'have', 'with', 'this', 'from', 'they', 'will', 'what', 'when', 'make', 'like', 'time', 'just', 'know', 'take', 'into', 'year', 'your', 'good', 'some', 'them', 'than', 'then', 'look', 'only', 'come', 'over', 'also', 'back', 'work', 'well', 'even', 'want', 'give', 'most']

#keys = guesskey(digrams, commondigrams)
#keys = guesskey(trigrams, commontrigrams)
keys = guesskey(['IDGM'], commonfourgrams)

test = 'KQOWEFVJPUJUUNUKGLMEKJINMWUXFQMKJBGWRLFNFGHUDWUUMBSVLPSNCMUEKQCTESWREEKOYSSIWCTUAXYOTAPXPLWPNTCGOJBGFQHTDWXIZAYGFFNSXCSEYNCTSSPNTUJNYTGGWZ'
key = 'SCUBA'
padded = key.ljust(5,'_')
print '%s : %s' % (padded, vigeneredecode(ciphertext, padded))

# doesn't seem to be english again
# used the frequency analysis tool on the black chamber and found the key in literally 10 seconds
# SCUBA
# it's the poem l'albatros by charles baudelaire



#vigenerelookup('I', 'T')
#vigenerelookup('D', 'H')
#vigenerelookup('G', 'E')
#vigenerelookup('M', 'N')
'''
K = "KLMNOPQRSTUVWXYZABCDEFGHIJ".lower()
Z = "ZABCDEFGHIJKLMNOPQRSTUVWXY".lower()
I = "IJKLMNOPQRSTUVWXYZABCDEFGH".lower()
N = "NOPQRSTUVWXYZABCDEFGHIJKLM".lower()
F = "FGHIJKLMNOPQRSTUVWXYZABCDE".lower()
U = "UVWXYZABCDEFGHIJKLMNOPQRST".lower()
Q = "QRSTUVWXYZABCDEFGHIJKLMNOP".lower()
'''
#print output
'''
key = []
key.append(K)
key.append(Z)
key.append(I)
key.append(abc)
key.append(abc)

output = ''
for i, c in enumerate(ciphertext):
    output += getpositionletter(getalphabetposition(c,key[i % 5]))

output = []
for n in xrange(len(key)):
    stringpart = list(texts[n])
    #print stringpart
    indexmap = dict(zip(stringpart,xrange(len(abc))))
    for i, c in enumerate(stringpart):
        stringpart[i] = getpositionletter(getalphabetposition(c,key[n]))
        #print "%s replaced with %s" % (c, getpositionletter(getalphabetposition(c,key[n])))
    output.append(stringpart)
'''
#print offsetcombine(texts)
