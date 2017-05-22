from collections import Counter
import re
ciphertext = "BT JPX RMLX PCUV AMLX ICVJP IBTWXVR CI M LMT'R PMTN, MTN YVCJX CDXV MWMBTRJ JPX AMTNGXRJBAH UQCT JPX QGMRJXV CI JPX YMGG CI JPX HBTW'R QMGMAX; MTN JPX HBTW RMY JPX QMVJ CI JPX PMTN JPMJ YVCJX. JPXT JPX HBTW'R ACUTJXTMTAX YMR APMTWXN, MTN PBR JPCUWPJR JVCUFGXN PBL, RC JPMJ JPX SCBTJR CI PBR GCBTR YXVX GCCRXN, MTN PBR HTXXR RLCJX CTX MWMBTRJ MTCJPXV. JPX HBTW AVBXN MGCUN JC FVBTW BT JPX MRJVCGCWXVR, JPX APMGNXMTR, MTN JPX RCCJPRMEXVR. MTN JPX HBTW RQMHX, MTN RMBN JC JPX YBRX LXT CI FMFEGCT, YPCRCXDXV RPMGG VXMN JPBR YVBJBTW, MTN RPCY LX JPX BTJXVQVXJMJBCT JPXVXCI, RPMGG FX AGCJPXN YBJP RAM"



# strip non-letters
cleanedtext = re.sub("[^a-zA-Z]+", "", ciphertext)

# count letters
letters = list(cleanedtext)
lettercount = Counter(letters)
print lettercount

# count instances of words
words = ciphertext.split()
counts = Counter(words)

# words of length N
N = 3
possible_words = [x for x in ciphertext.split() if len(x) == N]
print Counter(possible_words)

# N = 1 words
# M
# M is A or I
# N = 2 words
# CI 6, BT: 2, JC: 2, FX: 1, RC: 1, LX: 1
# we can probably assume CI is IT or ON
# N = 3 words
# JPX: 17, MTN: 8, PBR: 3, RAM: 1, YMR: 1, RMY: 1, CTX: 1, LXT: 1
# the frequency of J and X and the frequency of JPX indicates they're probably T and E respectively
# the rest was done by identifying words as they became apparent until the whole thing was solved
# 5:6-5:8
key = {'J': 't', 'P': 'h', 'X': 'e', 'C': 'o', 'R': 's', 'M': 'a', 'N': 'd', 'T': 'n', 'E': 'y', 'V': 'r', 'B': 'i', 'Y': 'w', 'W':'g', 'G': 'l', 'L': 'm', 'F': 'b', 'D': 'v', 'Q': 'p', 'I':'f', 'A': 'c', 'U': 'u', 'H': 'k', 'S': 'j'}

# Daniel 5:5-5:8 from the King James Bible

for cipherletter in key.keys():
    ciphertext = ciphertext.replace(cipherletter, key[cipherletter])
    #print "replaced %s with %s" % (cipherletter, key[cipherletter])

print ciphertext
