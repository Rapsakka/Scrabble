import time
import itertools

class Word:
    def __init__( self,word ):
        self.word = word #string of the word
        self.available = [*word]
        #self.neighbours = neighbours # Touple of neighbours i.e. other words and pivot chars i.e. conjuction point of words.
        self.pivot = self.pivots()
        self.connceted = False

    def pivots(self):
        pivots = list()
        for i in range(len( self.word)):
            pivots.append(False)
        return pivots

    def makeNeigbour(self, othWord ,char,place):
        if self.word[place] == char and self.pivot[place] == False :
            if ( place == 0 and self.pivot[place+1] == False ) :
                #self.neighbours.append( (othWord,place) )
                self.word =  self.word.replace(char,char.upper(),1) # ei toimi
                self.connceted = True
                self.pivot[place] = True
                return True
            elif place+1 == len(self.word) and self.pivot[place-1] == False :
                #self.neighbours.append((othWord, place))
                self.word = self.word.replace(char, char.upper(), 1)  # ei toimi
                self.connceted = True
                self.pivot[place] = True
                return True
            elif ( self.pivot[place-1] == False and self.pivot[place+1] == False ):
                #self.neighbours.append((othWord, place))
                self.word = self.word.replace(char, char.upper(), 1)  # ei toimi
                self.connceted = True
                self.pivot[place] = True
                return True
        return False

    def disconnect(self,char):
        e = self.available.index( char.lower() )
        del self.available[e]

    def __str__(self):
        return f"{self.word}"

def scrap() :
    f = open("Sanat.xml", "r")
    sanat = []
    for i in range(0,12):
        w = str(f.readline())

    while w != '':
        w = str(f.readline())
        c = w
        w = w.replace(" ", "")
        w = w.replace("<"," ")
        w = w.replace(">", " ")
        w = w.split()
        if len(w) < 3:
            break
        sanat.append(w[2])
    return sanat

def alphas(sana):
    a = ''.join(sorted(sana))
    return a

def breakDown(sana):
    kirjaimet = []
    for kir in sana: # hajotetaan sana kirjaimiin
        kirjaimet.append(kir)
    res = reduce(kirjaimet)
    avaimet = []
    for kirjain in res: #lasketaan jokaisen kirjaimen esiintymis taajuus
        maara = kirjaimet.count(kirjain) # lasketaan kirjaimen määrä
        avaimet.append((kirjain, maara))
    avaimet = frozenset( avaimet )
    return avaimet

def reduce(sana):
    res = []
    [res.append(x) for x in sana if x not in res]
    return res

def search(sana,dic): # all letter subsets that make up a word
    words = []
    for L in range(2,len(sana) + 1):
        for subset in itertools.combinations(sana, L):
            if breakDown(subset) in dic :
                for w in dic[breakDown(subset)]:
                    if w not in words:
                        words.append( w )

    return words

def combine(words,word): # yhdistelee sanoja jotta voidaan verrata taajuksia.
    matches = []
    brk = breakDown(word)   #liitoksia max len(subset)
    for L in range(2,len(word)//3):  # tähän voisi keksiä fiksumman
        if len(matches) > 20: # controls how many combos ( to reduce computation time)
            break
        for subset in itertools.combinations(words, L):
            ws = [] #list of acceptable subsets
            whole = ""
            flag = True
            subs = [Word(s) for s in subset ]
            for pairs in itertools.combinations(subs, 2):
                connect(pairs)
            for sub in subs:
                add = "".join( sub.available)
                #print(add)
                whole = whole+add
                #print(whole)
            for s in subs:
                ws.append(s)
                if s.connceted == False:
                    flag = False

            if ( len (whole)  == len(word) ):

                a = str(alphas(word)).lower()
                b = str( alphas(whole) ).lower()

                if a == b and flag == True:
                    matches.append(ws)
                    if len(matches) > 20:
                        break
    return matches

def connect(pair): # jos connectissa haluaa jotain muuttaa kannattaa muuttaa Word luokan metodeja
    p1 = pair[0]
    p2 = pair[1]

    for char, i in zip(  p1.word, range( 0,len(p1.word) ) ) :
        if char in p2.available and (not p2.connceted or not p1.connceted) :
            e = p2.available.index( char )
            if p1.makeNeigbour( p2 ,char, i ) and p2.makeNeigbour( p1, char, e ):
                p2.disconnect(char)

    return (p1,p2)

def routine(word,dic): #aeiiisssmpykkll # 15 char
    words = search(word, dic)
    results = combine(words, word)
    return results

if __name__ == '__main__':
    sanat = scrap()
    dic = {}
    for sana in sanat: # break down all Finnish words to their char freq
        freq = breakDown(sana)
        dic.setdefault(freq,[]).append(sana)
    while True:
        word = input("input any combination of charecters (end to quit): ")
        if word == "end":
            break
        fits = routine(word,dic)
        long = sorted(fits, key=len ,  reverse = True) # True many words, False few words
        for fit in long:
            print("parit")
            for f in fit:
                print(f)

            inp = input("do you want another resuly? Y/N")
            if inp == "N":
                break
    """
    word = "aeiikklss"
    combs = search(word,dic) #
    words = []
    for c in combs:
        if dic[breakDown(c)] not in words:
            words.append( dic[breakDown(c)] )
    wordsF = [item for sub_list in words for item in sub_list] #kaikki mahdolliset sanat
    potentials = combine( wordsF ,word )
    comb = []
    for pot in potentials:
        print(pot)
        comb.append( connect(pot) )
    """