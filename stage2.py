import re

# caesar shift cipher
ciphertext = "MHILY LZA ZBHL XBPZXBL MVYABUHL HWWPBZ JSHBKPBZ JHLJBZ KPJABT HYJHUBT LZA ULBAYVU"
letters = list(ciphertext)
orda = ord('A')

# brute force it
for shift in xrange(26):
    letters = list(ciphertext)
    for index, character in enumerate(letters):
        if(character != " "):
            letters[index] = chr(((ord(character) - orda) + shift) % 26 + orda)
    out = ''.join(letters)
    print 'shift: %s, text: %s' % (shift, out)

# just the solution
shift = 19
letters = list(ciphertext)
for index, character in enumerate(letters):
    if(character != " "):
        letters[index] = chr(((ord(character) - orda) + shift) % 26 + orda)
out = ''.join(letters)
print 'plaintext: %s' % (out)

# shift is at 19
# text is: FABER EST SUAE QUISQUE FORTUNAE APPIUS CLAUDIUS CAECUS DICTUM ARCANUM EST NEUTRON
