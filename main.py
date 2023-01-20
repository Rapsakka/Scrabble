import time
import itertools
from graphics import *

class Word:
    def __init__( self,word ):
        self.word = word #string of the word
        self.available = [*word]
        #self.neighbours = neighbours # Touple of neighbours i.e. other words and pivot chars i.e. conjuction point of words.
        self.pivot = self.pivots()
        self.connceted = False
        self.drawn = False

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
            subs = [Word(s) for s in subset ] #here strings are formed to words
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

def render(words):
    longest = 0
    sLongest = 0
    words.sort(key= lambda el: len(el.word))
    words.reverse()
    longest = len( words[0].word)
    sLongest = len(words[1].word)
    height = 150*sLongest    # korkeus
    width = 150*longest    #leveys
    win = GraphWin("Words",width,height)
    print()
    for pairs in itertools.combinations(words, 2):
        X = defineConjuction( ( pairs[0] , pairs[1] ) )
        Y = defineConjuction( ( pairs[1] , pairs[0] ) )
        if X[0] and Y[0]:
            if not pairs[0].drawn:
                for (char, place) in zip(pairs[0].word, range(0, len(pairs[0].word))):
                    name2 = "{charecter2}.gif".format(charecter2=pairs[0].word[place].upper())
                    img = Image(Point(120 + 120 * place, Y[1] * 120), name2)
                    img.draw(win)
                print(pairs[0].word)
                pairs[0].drawn = True
            if not pairs[1].drawn:
                for (char,place) in zip( pairs[1].word, range(0,len(pairs[1].word) )):
                    name = "{charecter}.gif".format(charecter = pairs[1].word[place].upper())
                    print(X[1]*120)
                    print(120+120*place)
                    img = Image( Point( X[1]*120, 120+120*place ), name )
                    img.draw(win)
                pairs[1].drawn = True
            pairs[0].pivot[X[1] - 1] = False
            pairs[1].pivot[Y[1] - 1] = False
            print(pairs[1].word)
            print()
    inp = input("close the grapichs Y/N?")
    while not inp == "Y" :
        inp = input("close the grapichs Y/N?")

    win.close

def defineConjuction(pWords):
    word1 = pWords[0]
    word2 = pWords[1]
    pivot1 = zip(word1.pivot,range(0,len(word1.pivot)) )
    pivot2 = zip(word2.pivot, range(0, len(word2.pivot)))
    for p1 in pivot1:
        if p1[0] :
            for p2 in pivot2:
                if p2[0]  and word1.word[ p1[1] ] == word2.word[ p2[1] ]:
                    return (True, p1[1]+1  )
    return (False,-1)

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
            print("Possible word combinations")
            for f in fit:
                print(f)
            render(fit)
            inp = input("do you want another resuly? Y/N")
            if inp == "N":
                break

