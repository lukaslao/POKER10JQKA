#Poker logic of a basic game of Poker on 'flet'
#by Lucas A. Oliveira

import random

def gerar_baralho():
    
    '''Function to generate the deck of cards and shuffle it
    with a VALUE on base 10, and a SUIT in a Single Number
    20 = 2, 30 = 3 ... 130 = K, 140 = A
    21 = two of hearts, 31 = three of hearts...
    44 = four of Spades... 144 = ACE of spades
    Hearts % 10  = 1
    Diamonds % 10 = 2
    Clubs % 10 = 3
    Spades % 10 = 4 
    '''

    copas = list(range(21,142,10))
    ouros = list(range(22,143,10))
    paus = list(range(23,144,10))
    espadas = list(range(24,145,10))
    deck = espadas + copas + ouros + paus
    random.shuffle(deck)
    return deck

embb = gerar_baralho() # Shuffled deck

print (embb)

#Hand of the players and the Table, following the deal order and discard one rules

maoplayer1 = [embb[0], embb[2]]
maoplayer2 = [embb[1], embb[3]]

flop = [embb[5],embb[6],embb[7]]
turn = [embb[9]]
river = [embb[11]]
mesa = flop + turn + river


#Hand of players combined with the Table

maop1f = maoplayer1 + mesa
maop2f = maoplayer2 + mesa

def cartaalta(x):

    """Put the numbers on a 10 base to rank them based on their VALUE
    ex: 21 = 20, 3 = 30, JACK = 110, ACE = 140"""
    
    rank = list(range(20,141, 10))
    a = list()    
    for carta in x:
        carta = (carta // 10) *10
        if carta in rank:
            a.append(carta)         
    return a

#Hands with only VALUE (High CARD)

maotp1rank = cartaalta(maop1f)
maotp2rank = cartaalta(maop2f)
mesarank = cartaalta(mesa)



def par(r, n) :

    """Search for a Pair in the hands"""

    pares = []
    for p, q in zip(r, n) :
        if r.count(p) == 2:
            pares.append(q)
    pares.sort(reverse=True)
    return pares

maop1pares = par(maotp1rank, maop1f)
maop2pares = par(maotp2rank, maop2f)
mesapares = par(mesarank, mesa)


def maofinalpar(p, n):

    """Take the previous function and defines the higher pair and the kicker"""

    rank = 0
    if len(p) == 2:
        hicard = list(set(n) - set(p))
        hicard.sort(reverse=True)
        maofinal = p + hicard
        maofinal = maofinal [0:5]
        rank = 1
    elif len(p) == 4:
        hicard = list(set(n) - set(p))
        hicard.sort(reverse=True)
        p.sort(reverse=True)
        maofinal = p + hicard
        maofinal = maofinal [0:5]
        rank = 2
    elif len(p) == 6:
        maofinal = p
        maofinal.sort(reverse=True)
        maofinal = maofinal[0:5]
        rank = 2
    else:
        maofinal = []
    return maofinal , rank


#hands if has a PAIR or TWO Pair
maoparp1 = maofinalpar(maop1pares, maop1f)
maoparp2 = maofinalpar(maop2pares, maop2f)
maoparmesa = maofinalpar(mesapares, mesa)

def parrank(r, n) :

    """Defining the RANK of the PAIRS 
    RANK RANGES (1pair) from 150 to 164 so it wins of HIGHCARD(ACE is 140)
    RANK RANGES (2pair) from 301 to 325 so it wins of a PAIR  
    PAIR OF 2's = 150, PAIR of ACES = 164
    TWO PAIRS,  SUM of two pairs  e.g: 2 and 2 = 150 + 4 and 4 = 152 = 302
    Highets two pair possible ACE/ACE KING/KING = 163 + 162 = 325
    FOUR OF a KIND(2 pairs equals) are another function"""

    pares = []
    for p, q in zip(r, n) :
        if r.count(p) == 2:
            pares.append(p)
    pares.sort(reverse=True)        
    return pares

def maoparrank(m, r, n):

    """Continues the last function"""

    if m[1] == 1:
        rank = 0
        pares = parrank(r, n)
        numero = list(range(20,141,10))
        rankpar = list(range(150,164))
        rankmao = 0
        for n, r in zip(numero, rankpar):
            if pares[0] == n:
                rankmao = r
    elif m[1] == 2:
        rank = 0
        pares = parrank(r, n)
        numero = list(range(20,141,10))
        rankpar = list(range(150,164))
        rankmao = 0
        for n, r in zip(numero, rankpar): 
            if pares[0] == n:
                rankmao = r
        for n, r in zip(numero, rankpar):
            if pares[2] == n:
                rankmao = rankmao + r 
    else:
        rankmao = 0
    return rankmao

#FINAL rank of PAIRS on hands 
rankpar1 = maoparrank(maoparp1, maotp1rank, maop1f)
rankpar2 = maoparrank(maoparp2, maotp2rank, maop2f)
rankmesapar = maoparrank(maoparmesa, mesarank, mesa)

#THREE of a kind
def trinca (r, n) :

    """Search for a 3 of a kind in hand"""

    trinca = []
    for p, q in zip(r, n) :
        if r.count(p) == 3:
            trinca.append(q)
    return trinca

maop1trinca = trinca(maotp1rank, maop1f)
maop2trinca = trinca(maotp2rank, maop2f)
mesatrinca = trinca(mesarank, mesa)



def maofinaltrinca(p, n):

    """Defines only the highest 3 of kind for the hand"""

    if len(p) == 3:
        hicard = list(set(n) - set(p))
        hicard.sort(reverse=True)
        maofinal = p + hicard
        maofinal = maofinal [0:5]
    #two three of kind in the total hand
    elif len(p) == 6:
        maofinal = p
        maofinal.sort(reverse=True)
        maofinal = maofinal[0:5]
    else:
        maofinal = []
    return maofinal

#FINAL Hand of the Three of a kinds
maotrincap1 = maofinaltrinca(maop1trinca, maop1f)
maotrincap2 = maofinaltrinca(maop2trinca, maop2f)
maotrincamesa = maofinaltrinca(mesatrinca, mesa)


def trincarank(r, n) :

    """Define the RANKS of 3's o kind    
    Turn the hand into its values: 20, 30 ,40...
    RANK RANGES from 350 to 353 so it wins of a 2 PAIR
    lowest 3ofkind of 2's = 350, 3's= 351 ....
    bigget 3ofkind ACE's = 363"""

    trinca = []
    for p, q in zip(r, n) :
        if r.count(p) == 3:
            trinca.append(p)
    trinca.sort(reverse=True)        
    return trinca

def maotrincarank(r, n):    
    trinca = trincarank(r, n)
    if not trinca :
        rankmao = 0
    else:
        numero = list(range(20,141,10))
        ranktrinca = list(range(350,364))
        rankmao = 0
        for n, r in zip(numero, ranktrinca):
            if trinca[0] == n:
                rankmao = r
    return rankmao

#FINAL rank of 3 of kind on hands 
ranktrinca1 = maotrincarank (maotp1rank, maop1f)
ranktrinca2 = maotrincarank(maotp2rank, maop2f)
ranktrincamesa = maotrincarank(mesarank, mesa)


#FOUR OF A KIND

def quadra (r, n) :

    """Search for a 4 of a kind in hands"""

    quadra = []
    for p, q in zip(r, n) :
        if r.count(p) == 4:
            quadra.append(q)
    return quadra

maop1quadra = quadra(maotp1rank, maop1f)
maop2quadra = quadra(maotp2rank, maop2f)
mesaquadra = quadra(mesarank, mesa)

#Defines the kicker
def maofinalquadra(p, n):
    if len(p) == 4:
        hicard = list(set(n) - set(p))
        hicard.sort(reverse=True)
        maofinal = p + hicard
        maofinal = maofinal [0:5]
    else:
        maofinal = []
    return maofinal

#FINAL hand of the FOUR of a Kind hand
maoquadp1 = maofinalquadra(maop1quadra, maop1f)
maoquadp2 = maofinalquadra(maop2quadra, maop2f)
maoquadmesa = maofinalquadra(mesaquadra, mesa)


def maoquadrank(s):

    '''Defines the RANK of the 4's of a kind
    ADDS 2000 RANK value to the sum of HAND so it wins of a FULLHOUSE
    RANK RANGES from 2110 to 2690
    Biggest possible 4'sofakind AAAAK = 140*4 + 130 = 690 +2000 = 2690
    lowest 4'ofakind possible 22223 = 20*4 + 30 = 110 +2000 = 2110'''

    rankmao = 0
    if not s:
        rankmao = 0
    else :
        rankear = cartaalta(s)
        rankmao = sum(rankear) + 2000
    return rankmao

#FINAL RANK of the quads
mao1quadrank = maoquadrank(maoquadp1)
mao2quadrank = maoquadrank(maoquadp2)
mesaquadrank = maoquadrank(maoquadmesa)



def sequencia(r, n):
    
    """Search for a sequence(STRAIGHT) of cards in hands(Values of cards)
    return sequence = ([seq], rank), ranking the seqs (NOT final RANK of hands)
    and returning only
    the highest sequence
    if hand total has (2 3 4 5 6 7 8), only 45678 valid
    highest possible seq 10 to Ace rank 10"""   

    rank = 0
    seq1 =  [140 , 20, 30, 40, 50, 0, 0] #ACE to 5's
    seq2 =  [20, 30, 40, 50, 60, 0 , 0]
    seq3 =  [30, 40, 50, 60, 70, 0 , 0]
    seq4 =  [40, 50, 60, 70, 80, 0 , 0]
    seq5 =  [50, 60, 70, 80, 90, 0 , 0]
    seq6 =  [60, 70, 80, 90, 100, 0 , 0]
    seq7 =  [70, 80, 90, 100, 110, 0 , 0]
    seq8 =  [80, 90, 100, 110, 120, 0 , 0]
    seq9 =  [90, 100, 110, 120, 130, 0 , 0]
    seq10 = [100, 110, 120, 130, 140, 0 , 0] #10 to ACES
    
    todasseq = [
        [*seq10],[*seq9],[*seq8],[*seq7],[*seq6],
        [*seq5],[*seq4],[*seq3],[*seq2],[*seq1]
        ]
    maoseq = []
    maonaipe = []
    
    for i in range(10):    
        if len(set(r)&set(todasseq[i])) == 5:
                maoseq = list(todasseq[i][0:5])
                rank = 10-i
                break
    for x in maoseq:
        for z in n:
            if z % x < 5:
                maonaipe.append(z)
 
    return  maonaipe, rank

#FINAL hand with sequence
maop1seq = sequencia(maotp1rank, maop1f)
maop2seq = sequencia(maotp2rank, maop2f)
mesaseq = sequencia(mesarank, mesa)


def maoseqrank(s):

    """RANK THE SEQUENCES(STRAIGHT)
    RANGES from 400 to 410 so it wins of 3 of a kinds
    LWST possible SEQ  ACE tO 5 RANK 400
    HIGHEST possible SEQ  10 TO ACE RANK 410"""

    if s[1] == 0:
        rankmao = 0
    elif s[1] > 0:
        rank = range(400,411)
        num = range(0, 11)
        for i, n in zip(num, rank):
            if s[1] == i:
                rankmao = n
    else:
        rankmao = 0
    return rankmao

#Final RANK of the seq HAND
mao1seqrank = maoseqrank(maop1seq)  
mao2seqrank = maoseqrank(maop2seq)  
maomesaseqrank = maoseqrank(mesaseq)  



def flush (f):

    """Searchs for a flush in hands
    5 cards with the Value + Suits equivalent number (20 + 1 = 2 of hearts)
    FLush of Hearts (1) : [21, 51, 91, 71, 101, 22, 44]...
    FLush of Spades (4) : [24, 54, 94, 74, 104, 21, 41]"""
    
    maosetf = set(f)
    setcopas = set(list(range(21,142,10)))
    setouros = set(list(range(22,143,10)))
    setpaus = set(list(range(23,144,10)))
    setespadas = set(list(range(24,145,10)))
    
    flushour = maosetf.intersection(setouros)
    flushcop = maosetf.intersection(setcopas)
    flushesp = maosetf.intersection(setespadas)
    flushpau = maosetf.intersection(setpaus)
    
    if len(flushesp) >= 5:
        maoflush = flushesp
    elif len(flushcop) >= 5:
        maoflush = flushcop
    elif len(flushpau) >= 5:
        maoflush = flushpau
    elif len(flushour) >=5:
        maoflush = flushour
    else:
        maoflush = []
    maoflush = list(maoflush)
    maoflush.sort(reverse = True)
    maoflush = maoflush [0:5]
    return maoflush

#FINAL Hand with the flush
maop1flush = flush(maop1f)
maop2flush = flush(maop2f)
mesaflush = flush(mesa)


def maoflushrank(s):

    """RANK the flushs
    ADDS 300 to the sum of values of cards
    RANGE from 500 to 900 so it wins of seq's    
    Lowest possible flush 60 50 40 30 20 =  RANK 200 + 300 = 500
    (straight FLUSH are not treated here, so this would be the lowest)
    HIGHEST possible FLUSH  140 to 100(Ace to 10) RANK 600 + 300 = 900
    (straight FLUSH are not treated here, so this would be the highest)"""

    if not s:
        rankmao = 0
    else :
        rankear = cartaalta(s)
        rankmao = 0
        rankmao = sum(rankear) + 300
    return rankmao

#FINAL rank of the flushs    
mao1flurank = maoflushrank(maop1flush)  
mao2flurank = maoflushrank(maop2flush)    
mesaflurank = maoflushrank(mesaflush) 


def maofhrank(p, t): 

    """RANK the FULL Houses
    Since is just a 3of a kind + a Pair, it gets the final hands if
    this former two are TRUE for a hand and rank the final hand
    ADDS 1000 to rank so it wins of FLUSHs
    RANGES from 1101 to 1231
    LOWESt possible fullhouse  22233 = rank 1000+101= 1101
    HIGHEST possible fullhouse AAAKK = rank 1120 + 111 = 1231"""

    rankmao = 0
    if not p :
        rankmao = 0
    elif not t:
        rankmao = 0
    elif p[1] > 0 and t[0] > 0:
        maofinalfh = t[0:3] + p[0][0:2]
        rankfh = cartaalta(maofinalfh)
        numero1 = list(range(20,141,10))
        rankt = list(range(1000,1121,10))
        rankp = list(range(100,113))
        rankmao = 0
        for n1,  r in zip(numero1, rankt):
            if rankfh[0] == n1: 
                rankmao = r
        for n1, r in zip(numero1, rankp):
            if rankfh[3] == n1:
                rankmao = rankmao + r
    return rankmao

#FINAL rank of fullhouse hand
maofh1rank = maofhrank(maoparp1, maop1trinca)
maofh2rank = maofhrank(maoparp2, maop2trinca)
maofhmesarank = maofhrank(maoparmesa, mesatrinca)

def straightflush(f):

    """
    Define the Rank of a Straight FLUSH
    similiar to FULLHOUSE, just gets the values of SEQUENCE and FLUSH
    and checks if its a STRAIGHT  with a FLUSH
    ADDS 3000 so it wins of quads and fullhouses
    LOWEST possible STRAIGHT FLUSH  AS,2,3,4,5  = RANK SEQ 1 * 3000 = 3000
    HIGHEST possible STRAIGHT FLUSH 
    ROYALFLUSH = 10,J,Q,K,A RANK SEQ 10 * 3000 = 30000 (BIGGEST SCORE POSSIBLE)"""

    rankmao = 0
    flushrank = cartaalta (f)
    flushseq = sequencia(flushrank, f)
    
    if flushseq[1] > 0:
        rankmao = flushseq[1] * 3000
    else:
        rankmao = 0
    return rankmao

#FINAL rank of the straight flush       
mao1strflurank = straightflush(maop1flush)
mao2strflurank = straightflush(maop2flush)
mesastrflurank = straightflush(mesaflush)

#Gets the MAX final RANK of any possible hand it may have
ranktotalp1 = max([
    rankpar1, ranktrinca1, maofh1rank, mao1seqrank,
    mao1flurank, mao1quadrank, mao1strflurank
    ])
ranktotalp2 = max([
    rankpar2, ranktrinca2, maofh2rank, mao2seqrank,
    mao2flurank, mao2quadrank, mao2strflurank
    ])
ranktotalm = max([
    rankmesapar, ranktrincamesa, maofhmesarank, maomesaseqrank,
    mesaflurank, mesastrflurank, mesaquadrank
    ])


print(f'''
Rank mao p1: {ranktotalp1}
Rank maop2: {ranktotalp2}
Rank mesa: {ranktotalm}''')

def nomesdasmaos(r):

    """Define the name of HANDS based on theirs ranks"""

    if r >= 150 and r <= 163:   
        mao = 'PAR'             #PAIR            
    elif r >= 300 and r<= 326:
        mao = '2 PARES'         #2PAIR
    elif r >= 350 and r<= 363:
        mao = 'TRINCA'          #THREE OF A KIND
    elif r >= 400 and r<= 410:
        mao = 'SEQUENCIA'       #SEQUENCE
    elif r >= 500 and r<= 900:
        mao = 'FLUSH'           #FLUSH
    elif r >= 1101 and r<= 1231:
        mao = 'FULL-HOUSE'      #FULLHOUSE
    elif r>= 2110 and r <= 2690:
        mao = 'QUADRA'          #FOUR OF A KIND
    elif r >= 3000 and r<= 27000:
        mao = 'STRAIGHT FLUSH'  
    elif r == 30000:
        mao = 'ROYAL FLUSH'
    else:
        mao = 'CARTA ALTA'      #HIGH-CARD
    return mao

#STRING with the name of the hands    
maop1string = nomesdasmaos(ranktotalp1) 
maop2string = nomesdasmaos(ranktotalp2) 
mesastring = nomesdasmaos(ranktotalm) 

print(f'Mesa: {mesa}')
print(f'Player 1 tem um: {maop1string}, {maoplayer1}')
print(f'Player 2 tem um: {maop2string}, {maoplayer2}')

#Finally decides a winner

vencedorrank = 0

if ranktotalp1 > ranktotalp2 and ranktotalp1 > ranktotalm:
    #winner PLAYER 1
    vencedorrank = ranktotalp1 
    vencedor = 'PLAYER1'
    print(f'player 1 venceu com um {maop1string}')
elif ranktotalp1 < ranktotalp2 and ranktotalp2 > ranktotalm:
    #winner PLAYER 2
    vencedorrank = ranktotalp2
    vencedor = 'PLAYER2'
    print(f'player 2 venceu com um {maop2string}')
elif ranktotalm > ranktotalp1 and ranktotalm > ranktotalp2:
    #TABLE owned both so its a direct DRAW
    vencedorrank = ranktotalm
    vencedor = 0
    print(f'Empate {mesastring}')
    
elif ranktotalp1 == ranktotalp2:
        
        #Futher check draws conditions 
        
        if maop1string == 'CARTA ALTA': #BOTH have highcards, check everycard
            maop1f.sort(reverse=True)
            maop2f.sort(reverse=True)
            maoempatep1 = cartaalta(maop1f)
            maoempatep2 = cartaalta(maop2f)
            
            for p1,p2 in zip(maoempatep1,maoempatep2):
                if p1 > p2:
                    vencedorrank = ranktotalp1
                    vencedor = 'PLAYER1'
                    break
                elif p1 < p2:
                    vencedorrank = ranktotalp2
                    vencedor = 'PLAYER2'
                    break            
                elif p1 == p2:
                    vencedorrank = 0
                    vencedor = 0  
        
        elif maop1string == 'PAR': #BOTH have the SAME PAIR
            
            maoempatep1 = cartaalta(maoparp1[0][2:])
            maoempatep2 = cartaalta(maoparp2[0][2:])
            for p1,p2 in zip(maoempatep1,maoempatep2):
                if p1 > p2:
                    vencedorrank = ranktotalp1
                    vencedor = 'PLAYER1'
                    break
                elif p1 < p2:
                    vencedorrank = ranktotalp2
                    vencedor = 'PLAYER2'
                    break
                elif p1 == p2:
                    vencedorrank = 0
                    vencedor = 0    
        
        elif maop1string == '2 PARES': #BOTH have the SAME 2 PAIR
            
            maoempatep1 = cartaalta(maoparp1[0])
            maoempatep2 = cartaalta(maoparp2[0])
            
            if maoempatep1[-1] > maoempatep2[-1]:
                vencedorrank = ranktotalp1
                vencedor = 'PLAYER1'
                
            elif maoempatep1[-1] < maoempatep2[-1]:
                vencedorrank = ranktotalp2
                vencedor = 'PLAYER2'
                
            else:
                vencedorrank = 0
                vencedor = 0

        elif maop1string == 'TRINCA': 
            
            #BOTH have the SAME 3 of a kind, 
            #it happens, and more often than you think..
            
            maoempatep1 = cartaalta(maotrincap1)
            maoempatep2 = cartaalta(maotrincap2)
            
            for p1,p2 in zip(maoempatep1,maoempatep2):
                if p1>p2:
                    vencedorrank = ranktotalp1
                    vencedor = 'PLAYER1'
                    break
                elif p1<p2:
                    vencedorrank = ranktotalp2
                    vencedor = 'PLAYER2'
                    break
                elif p1 == p2:
                    vencedorrank = 0
                    vencedor = 0 
        print(f'{vencedor} venceu com um {maop1string}') 



def melhorrank(mao):

    """Runs all the functions on one hand and returns its MAX rank"""
    
    melhorhc = cartaalta(mao)
    melhorpares = par(melhorhc, mao)
    melhorpares2 = maofinalpar(melhorpares, mao)
    melhorrankpar = maoparrank(melhorpares2, melhorhc, mao)
    maomtrinca = trinca(melhorhc, mao)
    maomelhortrinca = maofinaltrinca(maomtrinca, mao)
    ranktrincamelhor = maotrincarank (melhorhc, mao)
    maomelhorquad = quadra(melhorhc, mao)
    maoquadmelhor = maofinalquadra(maomelhorquad, mao)
    maoquadrankmelhor = maoquadrank(maoquadmelhor)
    maomelhorseq = sequencia(melhorhc, mao)
    maomelhorseqrank = maoseqrank(maomelhorseq)  
    maomelhorflush = flush(mao)
    maomelhorflurank = maoflushrank(maomelhorflush)
    maomelhorfhrank = maofhrank(melhorpares2, maomtrinca)
    maomelhorstrflurank = straightflush(maomelhorflush)
    
    maiorrank = max([
        melhorrankpar,ranktrincamelhor,maoquadrankmelhor,
        maomelhorfhrank,maomelhorflurank,
        maomelhorseqrank,maomelhorstrflurank
        ])
    
    return maiorrank
    
best_hand = mesa #The best possible hand starts with only the table
best_rankpossb = 0 #rank to beat, could be player 1 ranktotalp1 and add a break to its if
best_hand_final = []

#make all non used cards iterables between each other and finds the max rank
#possible whithin this table

for carta1 in embb:    
    if carta1 not in maop1f:
        best_hand.append(carta1)
        for carta2 in embb:
            if carta2 not in best_hand and carta2 not in maop1f:
                best_hand.append(carta2)
                maiorrank = melhorrank(best_hand)
                if maiorrank > ranktotalp1: 
                    #if set to > best_rankpossb var it will always get the best possible hand
                    #here it beats only player1                   

                    best_rankpossb = maiorrank
                    best_hand_final = []
                    best_hand_final = best_hand[:]                    
                    best_hand.pop()
                    
                else:                    
                    best_hand.pop()
        else:
            best_hand.pop()       
                    
print('melhor mao possivel: ', best_hand_final) #Best possible hand + table
print('Rank: ' ,best_rankpossb)
print(f'{nomesdasmaos(best_rankpossb)}')
