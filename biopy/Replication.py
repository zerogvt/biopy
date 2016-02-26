
bioText = "ATCAATGATCAACGTAAGCTTCTAAGCATGATCAAGGTGCTCACACAGTTTATCCACAACCTGAGTGGATGACATCAAGATAGGTCGTTGTATCTCCTTCCTCTCGTACTCTCATGACCACGGAAAGATGATCAAGAGAGGATGATTTCTTGGCCATATCGCAATGAATACTTGTGACTTGTGCTTCCAATTGACATCTTCAGCGCCATATTGCGCTGGCCAAGGTGACGGAGCGGGATTACGAAAGCATGATCATGGCTGTTGTTCTGTTTATCTTGTTTTGACTGAGACTTGTTAGGATAGACGGTTTTTCATCACTGACTAGCCAAAGCCTTACTCTGCCTGACATCGACCGTAAATTGATAATGAATTTACATGCTTCCGCGACGATTTACCTCTTGATCATCGATCCGATTGAAGATCTTCAATTGTTAATTCTCTTGCCTCGACTCATAGCCATGATGAGCTCTTGATCATGTTTCCTTAACCCTCTATTTTTTACGGAAGAATGATCAAGCTGCTGCTCTTGATCATCGTTTC"
k=10
bioPattern = "TGT"

def PatternCount(pat, txt):
    count = 0
    for i in range(0,len(txt)-len(pat)+1):
        if pat==txt[i:i+len(pat)] :
            count+=1
    return count

def PatternCount2(pat, txt):
    count = 0
    positions = []
    for i in range(0,len(txt)-len(pat)+1):
        #print txt[i:i+len(pat)]
        if pat==txt[i:i+len(pat)] :
            count+=1
            positions.append(i)
    return positions

def FrequentWords(Text, k):
    FrequentPatterns = set()
    Count = CountDict(Text, k)
    m = max(Count.values())
    for i in Count:
        if Count[i] == m:
            FrequentPatterns.add(Text[i:i+k])
    return FrequentPatterns




def CountDict(Text, k):
    Count = {}
    for i in range(len(Text)-k+1):
        Pattern = Text[i:i+k]
        Count[i] = PatternCount(Pattern, Text)
    return Count
           
           
def ReverseComplement(dnatxt):
    rev = ""
    c=''
    strand = dnatxt.upper()
    for n in strand[::-1]:
        if  n == 'A': 
            c = 'T'
        elif n == 'T':
            c = 'A'
        elif n == 'G':
            c = 'C'
        elif n == 'C':
            c = 'G'
        else :
            c = '-'
        rev += str(c)
    return rev


def SymbolArray(Genome, symbol):
    n = len(Genome)
    array = {}
    ExtendedGenome = Genome + Genome[0:n//2]
    print ExtendedGenome
    array[0] = PatternCount(symbol, ExtendedGenome[0:n//2] )
    for i in range( 1, n):
        array[i] = array[i-1]
        if ExtendedGenome[i-1]==symbol:
            array[i] -= 1
        if ExtendedGenome[i+n//2]==symbol:
            array[i] += 1
        
    return array
    

def Skew(Genome):
    s = {}
    s[0]=0
    for i in range(1,len(Genome)+1):
        if Genome[i-1]=="G":
            s[i] = s[i-1]+1
        elif Genome[i-1]=="C":
            s[i] = s[i-1]-1
        else:
            s[i] = s[i-1]
    return s

def MinimumSkew(Genome):
    s = Skew(Genome)
    m = s.get(min(s, key=s.get))
    minarray = []
    for k in s:
        if s[k]==m:
            minarray.append(k)
    return minarray

def MaximumSkew(Genome):
    s = Skew(Genome)
    m = s.get(max(s, key=s.get))
    maxarray = []
    for k in s:
        if s[k]==m:
            maxarray.append(k)
    return maxarray
    
def HammingDistance(p, q):
    if len(p)!=len(q):
        return -1
    dist = 0
    for i in range(0, len(p)):
        if p[i]!=q[i]:
            dist += 1
    return dist


def ApproximatePatternCount(pat, txt, distance):
    count = 0
    positions = []
    for i in range(0,len(txt)-len(pat)+1):
        #print txt[i:i+len(pat)]
        if HammingDistance(pat, txt[i:i+len(pat)])<=distance :
            count+=1
            positions.append(i)
    return positions

def ApproximatePatternMatching(pat, txt, distance):
    count = 0
    positions = []
    for i in range(0,len(txt)-len(pat)+1):
        #print txt[i:i+len(pat)]
        if HammingDistance(pat, txt[i:i+len(pat)])<=distance :
            count+=1
            positions.append(i)
    return len(positions)


def FrequentWordsWithFreq(Text, k, freq):
    FrequentPatterns = set()
    Count = CountDict(Text, k)
    for i in Count:
        if Count[i] >= freq:
            FrequentPatterns.add(Text[i:i+k])
    return FrequentPatterns


#########################################################
#LESSON 3 - motifs
def Count(Motifs):
    count={}
    k = len(Motifs[0])
    for symbol in "ACGT":
        count[symbol] = []
        for j in range(k):
            count[symbol].append(0)
    t = len(Motifs)
    for i in range(t):
        for j in range(k):
            symbol = Motifs[i][j]
            count[symbol][j] += 1
    return count

def Profile(Motifs):
    k = len(Motifs[0])
    h = len(Motifs)
    profile = Count(Motifs)
    for symbol in "ACGT":
        for j in range(k):
            profile[symbol][j] = profile[symbol][j]/float(h)
    return profile


def Consensus(Motifs):
    prof = Count(Motifs)
    k = len(Motifs[0])
    concensus=[]
    for i in range(k):
        maxp = 0.0
        for symbol in "ACGT":
            if prof[symbol][i] > maxp:
                maxp = prof[symbol][i]
                maxsym = symbol
        concensus.append(maxsym)    
    return ''.join(concensus)    

def Score(Motifs):
    con = Consensus(Motifs)
    k = len(Motifs[0])
    h = len(Motifs)
    score = 0
    for i in range(k):
        for j in range(h):
            if Motifs[j][i] != con[i]:
                score += 1
    return score

def Pr(Text, Profile):
    p = 1.0
    for i in range(len(Text)):
        symbol = Text[i] 
        p = p * Profile[symbol][i]
    return p


def ProfileMostProbablePattern(Text, k, Profile):
    p = -1.0
    winner = Text[0:k]
    for i in range(len(Text)-k+1):
        kmer = Text[i:i+k]
        pkmer = Pr(kmer, Profile)
        if pkmer > p:
            p = pkmer
            winner = kmer
    return winner

#Dna
#kmer motif

def GreedyMotifSearch(Dna, k, t):
    BestMotifs = []
    for i in range(0, t):
        BestMotifs.append(Dna[i][0:k-1])
    n = len(Dna[0])
    for i in range(n-k+1):
        Motifs = []
        Motifs.append(Dna[0][i:i+k])
        for j in range(1, t):
            P = Profile(Motifs[0:j])
            Motifs.append(ProfileMostProbablePattern(Dna[j], k, P))    
        if Score(Motifs) < Score(BestMotifs):
            BestMotifs = Motifs
    return BestMotifs
#

def CountWithPseudocounts(Motifs):
    count={}
    k = len(Motifs[0])
    for symbol in "ACGT":
        count[symbol] = []
        for j in range(k):
            count[symbol].append(1)
    
    t = len(Motifs)
    for i in range(t):
        for j in range(k):
            symbol = Motifs[i][j]
            count[symbol][j] += 1
    return count

def ProfileWithPseudocounts(Motifs):
    k = len(Motifs[0])
    h = len(Motifs)
    profile = CountWithPseudocounts(Motifs)
    for symbol in "ACGT":
        for j in range(k):
            profile[symbol][j] = (profile[symbol][j])/float(4+h)
    return profile

def GreedyMotifSearchWithPseudocounts(Dna, k, t):
    t = len(Dna)
    BestMotifs = []
    for i in range(0, t):
        BestMotifs.append(Dna[i][0:k-1])
    n = len(Dna[0])
    for i in range(n-k+1):
        Motifs = []
        Motifs.append(Dna[0][i:i+k])
        for j in range(1, t):
            P = ProfileWithPseudocounts(Motifs[0:j])
            Motifs.append(ProfileMostProbablePattern(Dna[j], k, P))    
        if Score(Motifs) < Score(BestMotifs):
            BestMotifs = Motifs
    return BestMotifs

def PKmer(Profile, kmer):
    p = 1.0;
    for i in range(len(kmer)):
        symbol = kmer[i]
        p = p * Profile[symbol][i];
    return p;

def Motifs(Profile, Dna):
    k = len(Profile['A'])
    kmermax = {}
    for h in range(len(Dna)):
        pmax=0.0;
        for i in range(len(Dna[0])-k+1):
            kmer = Dna[h][i:i+k]
            p = PKmer(Profile, kmer)
            if p >= pmax:
                pmax = p
                kmermax[h] = kmer
    ret=[]
    for h in range(len(Dna)):
        ret.append(kmermax[h])          
    return ret

import random

def RandomMotifs(Dna, k, t):    
    t = len(Dna)
    kmers = []
    for h in range( t ):
        i = random.randint(0, len(Dna[0])-k);
        kmers.append( Dna[h][i:i+k] )
    return kmers


def RandomizedMotifSearch(Dna, k, t):
    t = len(Dna)
    M = RandomMotifs(Dna, k, t)
    BestMotifs = M
    while True:
        Profile = ProfileWithPseudocounts(M)
        M = Motifs(Profile, Dna)
        if Score(M) < Score(BestMotifs):
            BestMotifs = M
        else:
            return BestMotifs 
 

Dna = {0: "GCGCCCCGCCCGGACAGCCATGCGCTAACCCTGGCTTCGATGGCGCCGGCTCAGTTAGGGCCGGAAGTCCCCAATGTGGCAGACCTTTCGCCCCTGGCGGACGAATGACCCCAGTGGCCGGGACTTCAGGCCCTATCGGAGGGCTCCGGCGCGGTGGTCGGATTTGTCTGTGGAGGTTACACCCCAATCGCAAGGATGCATTATGACCAGCGAGCTGAGCCTGGTCGCCACTGGAAAGGGGAGCAACATC", 
       1: "CCGATCGGCATCACTATCGGTCCTGCGGCCGCCCATAGCGCTATATCCGGCTGGTGAAATCAATTGACAACCTTCGACTTTGAGGTGGCCTACGGCGAGGACAAGCCAGGCAAGCCAGCTGCCTCAACGCGCGCCAGTACGGGTCCATCGACCCGCGGCCCACGGGTCAAACGACCCTAGTGTTCGCTACGACGTGGTCGTACCTTCGGCAGCAGATCAGCAATAGCACCCCGACTCGAGGAGGATCCCG", 
       2: "ACCGTCGATGTGCCCGGTCGCGCCGCGTCCACCTCGGTCATCGACCCCACGATGAGGACGCCATCGGCCGCGACCAAGCCCCGTGAAACTCTGACGGCGTGCTGGCCGGGCTGCGGCACCTGATCACCTTAGGGCACTTGGGCCACCACAACGGGCCGCCGGTCTCGACAGTGGCCACCACCACACAGGTGACTTCCGGCGGGACGTAAGTCCCTAACGCGTCGTTCCGCACGCGGTTAGCTTTGCTGCC", 
       3: "GGGTCAGGTATATTTATCGCACACTTGGGCACATGACACACAAGCGCCAGAATCCCGGACCGAACCGAGCACCGTGGGTGGGCAGCCTCCATACAGCGATGACCTGATCGATCATCGGCCAGGGCGCCGGGCTTCCAACCGTGGCCGTCTCAGTACCCAGCCTCATTGACCCTTCGACGCATCCACTGCGCGTAAGTCGGCTCAACCCTTTCAAACCGCTGGATTACCGACCGCAGAAAGGGGGCAGGAC", 
       4: "GTAGGTCAAACCGGGTGTACATACCCGCTCAATCGCCCAGCACTTCGGGCAGATCACCGGGTTTCCCCGGTATCACCAATACTGCCACCAAACACAGCAGGCGGGAAGGGGCGAAAGTCCCTTATCCGACAATAAAACTTCGCTTGTTCGACGCCCGGTTCACCCGATATGCACGGCGCCCAGCCATTCGTGACCGACGTCCCCAGCCCCAAGGCCGAACGACCCTAGGAGCCACGAGCAATTCACAGCG", 
       5: "CCGCTGGCGACGCTGTTCGCCGGCAGCGTGCGTGACGACTTCGAGCTGCCCGACTACACCTGGTGACCACCGCCGACGGGCACCTCTCCGCCAGGTAGGCACGGTTTGTCGCCGGCAATGTGACCTTTGGGCGCGGTCTTGAGGACCTTCGGCCCCACCCACGAGGCCGCCGCCGGCCGATCGTATGACGTGCAATGTACGCCATAGGGTGCGTGTTACGGCGATTACCTGAAGGCGGCGGTGGTCCGGA", 
       6: "GGCCAACTGCACCGCGCTCTTGATGACATCGGTGGTCACCATGGTGTCCGGCATGATCAACCTCCGCTGTTCGATATCACCCCGATCTTTCTGAACGGCGGTTGGCAGACAACAGGGTCAATGGTCCCCAAGTGGATCACCGACGGGCGCGGACAAATGGCCCGCGCTTCGGGGACTTCTGTCCCTAGCCCTGGCCACGATGGGCTGGTCGGATCAAAGGCATCCGTTTCCATCGATTAGGAGGCATCAA", 
       7: "GTACATGTCCAGAGCGAGCCTCAGCTTCTGCGCAGCGACGGAAACTGCCACACTCAAAGCCTACTGGGCGCACGTGTGGCAACGAGTCGATCCACACGAAATGCCGCCGTTGGGCCGCGGACTAGCCGAATTTTCCGGGTGGTGACACAGCCCACATTTGGCATGGGACTTTCGGCCCTGTCCGCGTCCGTGTCGGCCAGACAAGCTTTGGGCATTGGCCACAATCGGGCCACAATCGAAAGCCGAGCAG", 
       8: "GGCAGCTGTCGGCAACTGTAAGCCATTTCTGGGACTTTGCTGTGAAAAGCTGGGCGATGGTTGTGGACCTGGACGAGCCACCCGTGCGATAGGTGAGATTCATTCTCGCCCTGACGGGTTGCGTCTGTCATCGGTCGATAAGGACTAACGGCCCTCAGGTGGGGACCAACGCCCCTGGGAGATAGCGGTCCCCGCCAGTAACGTACCGCTGAACCGACGGGATGTATCCGCCCCAGCGAAGGAGACGGCG", 
       9: "TCAGCACCATGACCGCCTGGCCACCAATCGCCCGTAACAAGCGGGACGTCCGCGACGACGCGTGCGCTAGCGCCGTGGCGGTGACAACGACCAGATATGGTCCGAGCACGCGGGCGAACCTCGTGTTCTGGCCTCGGCCAGTTGTGTAGAGCTCATCGCTGTCATCGAGCGATATCCGACCACTGATCCAAGTCGGGGGCTCTGGGGACCGAAGTCCCCGGGCTCGGAGCTATCGGACCTCACGATCACC"
       }

N=100
k=15
t=10
for i in range(N):
    M = RandomizedMotifSearch(Dna, k, t)
    if i==0:
        BestMotifs = M
        maxScore = Score(M)
    else:
        if Score(M) >= maxScore:
            BestMotifs = M
            maxScore = Score(M)

print (BestMotifs)
print (Score(BestMotifs))

            
profile={'A':[0.8, 0.0, 0.0, 0.2],
'C':[0.0, 0.6, 0.2, 0.0],
'G':[0.2, 0.2, 0.8, 0.0],
'T':[0.0, 0.2, 0.0, 0.8]
         }
lines=[]
lines.append("TTACCTTAAC")
lines.append("GATGTCTGTC")
lines.append("ACGGCGTTAG")
lines.append("CCCTAACGAG")
lines.append("CGTCAGAGGT")
#print (ProfileWithPseudocounts(lines))

Dna2={0:"CGCCCCTCTCGGGGGTGTTCAGTAAACGGCCA",
1:"GGGCGAGGTATGTGTAAGTGCCAAGGTGCCAG",
2:"TAGTACCGAGACCGAAAGAAGTATACAGGCGT",
3:"TAGATCAAGTTTCAGGTGCACGTCGGTGAACC",
4:"AATCCACCAGCTCCACGTGCAATGTTGGCCTA",
}



#print(Motifs(profile, lines))
#print (RandomizedMotifSearch(Dna, 8, 5))

#print(GreedyMotifSearchWithPseudocounts(lines, 3, 5))

#Dna={0:lines[0], 1:lines[1], 2:lines[2], 3:lines[3], 4:lines[4]}

#print(GreedyMotifSearchWithPseudocounts(Dna, 15, 10))
#A = [float(c) for c in lines[0].split()]
#C = [float(c) for c in lines[1].split()]
#G = [float(c) for c in lines[2].split()]
#T = [float(c) for c in lines[3].split()]
#Prof = {'A':A, 'C':C, 'G':G, 'T':T}
#print (GreedyMotifSearch(Dna, 15, 10))
#print(ProfileMostProbablePattern("ACCTGTTTATTGCCTAAGTTCCGAACAAACCCAATATAGCCCGAGGGCCT",5, Prof))

    
#print( Consensus( ["AACGTA","CCCGTT","CACCTT","GGATTA","TTCCGG"] ))
#print (Score (["GGCTCGAAAC","GCCTATACTG","GCTGGGCAAA","GGACGAGACC","AGCGATTTAC","GGCCGCCGTG","AATGCATATT","GTTCTCCGTT","TAGATCGTAT","ACCGGGAAGG"]) )

#print HammingDistance("CTTGAAGTGGACCTCTAGTTCCTCTACAAAGAACAGGTTGACCTGTCGCGAAG", "ATGCCTTACCTAGATGCAATGACGGACGTATTCCTTTTGCCTCAACGGCTCCT")
#print PatternCount2("AGCGTCCAG","AGCGTCCAGCGTCCCAGCGTCCTGAGCGTCCGTAGCGTCCAGCGTCCTGAGCGTCCAAAGCGTCCAGCGTCCAAGCAACAGCGTCCAGCGTCCTACAGCGTCCAGACGAGCGTCCCAGCGTCCAGCGTCCGATTAGCGTCCAGCGTCCAGCGTCCATTTTAAAGCGTCCCTCGAGCGTCCAGCGTCCTGTCAGATAGCGTCCCAAGCGTCCGAGCGTCCTAGAATCAGCGTCCGCAAGAAGCGTCCAGCGTCCTGAGCGTCCAAGCGTCCTAGCGTCCCCAAGCGTCCCTGAAGCGTCCCAGCGTCCGACGGGAGCGTCCCGCAGCGTCCACAGCGTCCCAAGCGTCCTAGCGTCCAATAGCGTCCGCTAGCGTCCAGCGTCCTAGCGTCCAGCGTCCTAGAGCGTCCGTATATCAGCGTCCAGCGTCCGAAGAGCGTCCTCCTAGCGTCCGTTCTAAATTCTAGCGTCCGAGCGTCCTATCCGTCATTAGCGTCCGAGCGTCCTAGCGTCCTAGTCAGCGTCCAGCGTCCCTATTCTGAGCGTCCAGCGTCCTTAAGCGTCCAGCGTCCCTCGTAGCGTCCGGATAAACGCAAGCGTCCGCAGCGTCCCCGAGCGTCCGACCTAAAGGCAGCGTCCACGAGTAGCGTCCCGGAACAAGCGTCCAGTGGTAGCGTCCGAGCGTCCCAAAGCGTCCCACTAGCGTCCAGCGTCCACCAAAGCGTCCAAGCGTCCGAGCGTCCAGCGTCCGAGAAGCGTCCAGCGTCCAAGCGTCCATAGCGTCCGTAGAGCGTCCCCTCCTGCAAAGCGTCCAGCGTCCAGAGCGTCCGAAGCGTCCTAGCGTCCGATAGCGTCCCGAGAAGCGTCCGAGCGTCCTAGTTAGCGTCCTCTAGAGCGTCCAGCGTCCTGGTATTAGCGTCCCCCGCAGCGTCCCCTATAGCGTCCGAGCGTCCAATCCAGCGTCCGGCAGCGTCCGAACGAGCGTCCAGCGTCCTTAGCGTCCAGCGTCCAAGCGTCCAGCGTCCTTGTCGTTTGAGAGCGTCCAAGCGTCCAGCGTCCAGCGTCCAGCGTCCAGCGTCCAGCGTCCGAGCGTCCAAGCGTCCTGGAGCGTCCAGAGCGTCCAAGCGTCCACCCATAGCGTCCGCTCCCTCAGCAAGCGTCCATGAGCGTCCATTCAAAGCGTCCAGCGTCCAGCGTCCGTGATATGCAAGCGTCCGTAGCATCGAAAGCGTCCAGCGTCCTTAGCGTCCAGCGTCCAGCGTCCCATAGCGAGCGTCCAGCGTCCAGCGTCCTGAATAGCGTCCAAGCGTCCATAGCGTCCTAGGTAGCGTCCCTAGCGTCCCCAGCGTCCTTGGTAACGAGCGTCCCCTTGCAAAGCGTCCATTGAGCGTCCTCAGCGTCCTGAGCGTCCGAAGCGTCCAGCGTCCAGCGTCCAGCGTCCAAGCGTCCGGTTAGCGTCCCGAGCGTCCAGCGTCCGCCACAGCGTCCAGCTCACCGGGGCACAAGCGTCCAGCGTCCCGAAGCGTCCTGGAATGGGTAGCGTCCCAGCGTCCCAAAAGCGTCCGTGCCGAGCGTCCATACAGCGTCCAGCGTCCCGAAATAGCGTCCCGACTTTGTTAGCGTCCGAGCGTCCATAAATTAGCGTCCAGCGTCCGCTGTAGCGTCCAAGCGTCCAGCGTCCGAGCGTCCATGATCAGCGTCCTAAGCGTCCACCAAGCGTCCTCCGAAGCGTCCTTGTAGCGTCCCAGCGTCCGAGCGTCCAGCGTCCTCAGTATAGCGTCCCAGCGTCCCAGCGTCCAGCGTCCAGCGTCCCCAGCGTCCAGCGTCCAACCAGCGTCCGGGAGCGTCCCATAGCGTCCAGCGTCCAGCGTCCTCCTTAGCGTCCAGCGGAGCGTCCTGAGCGTCCCGTAAATAGCGTCCAGCGTCCAGCGTCCCCCCGAATAGCGTCCAGCGTCCAAAGCGTCCCAGCGTCCATAAGCGTCCACCCCCCATATCTAGCGTCCTAGCGTCCTTACGAAGCCCGAGCGTCCCAAAGAGCGTCCGGTTAACACGGCATTAGCGTCCTTATTTTAGCGTCCGAGCGTCCCAGCGTCCTAGCAGCGTCCCTAGCAGCGTCCAAGCGTCCACAGCGTCCAGCGTCCCTGCAAGCGTCCAGCGTCCCGCTAGCGTCCAGCGTCCGTAGCGTCCTAGCGTCCAGCGTCCATGCTAGCGTCCAGCGTCCAGGAGCGTCCCAGCGTCCAGCGTCCCCAGCGTCCAGCGTCCATGTAGCGTCCACCAGCGTCCCAGGATAGCGTCCAAGCGTCCTAAGCGTCCACGCGACGCGATAGCGTCCAGCGTCCGCAGCGTCCAGCGTCCGCCACTAGCGTCCCAGCGTCCAGCGTCCCAGCGTCCAGCGTCCAACCAGCGTCCTTGAGCGTCCACAGCGTCCGCTCAAAGCGTCCGAGCGTCCCTGGAAGCGTCCATTCCTGCGATTTAGAGCGTCCCTCATAGAGCGTCCAAAGCGTCCCTAGCGTCCAGCGTCCATCCAGCGTCCGTTCGTAGCGTCCTAGCAGCGTCCCTGAGCGTCCGAGCGTCCAGCGTCCAGCGTCCGACCAAGCGTCCAAGCGTCCAGCAGCGTCCTTGCGGAAGCGTCCTGACTCAGCGTCCAGCGTCCTGTCCTGAGTACAGCGTCCATGAAGCGTCCCTGTCTAGCGTCCGAGCGTCCTAGCGTCCTACGTCTCCGGCGAAGCGTCCCTCGTGGCCAAGCGTCCCAAGCGTCCTGCAGCGTCCAGCGTCCGATCACAGCGTCCCCCCAGCGTCCTAGCGTCCAGGTAGCGTCCAGCGTCCCCAGCGTCCTAGCGTCCTGTACGCAGCGTCCAGCGTCCGAGCGTCCCCGGTACTTTCCTGAAGCGTCCTCAAGCGTCCTATTTTAGCGTCCGCTTAAGCGTCCGTAGCGTCCTAAGCGTCCGAGCGTCCTGTATCTGAGGCGTAGCGTCCGGCAGCGTCCAAGCGTCCAGCGTCCAGCGAGCGTCCAGCGTCCAGCGTCCGTAGCGTCCGCAGCGTCCAGCGTCCGAGGAGCGTCCAGCGTCCGAGCGTCCCGAGCGTCCAGCGTCCTCGTCCAGCGTCCTAGCATGTAGCGTCCTATGATGGTAGTGGTCAGCGTCCTAGCGTCCTTAGCGTCCATACAGCGTCCCTCCCCAGCGTCCTGGAGCCTATGTCAGTTCCCTCGAGCGTCCTTTATCAATGAGCGTCCGCTTCAGCGTCCCAGCGTCCTAGCGTCCGACCAAGCGTCCAGCGTCCGTCAACAGCGTCCACAGCGTCCACAGAGAGCGTCCAGCGTCCGATAGCGTCCAGCGTCCCCGGTAGCGTCCAGCGTCCAAGCGTCCAGCGTCCATAACGAGCGTCCCAGCGTCCGTCTTGAGCGTCCCAGCGTCCTGTAGCGTCCACTACTTTTTGGAGCGTCCGAGCGTCCAGCGTCCCGAACTGCGCAGCGTCCCAGCGTCCCCAGCGTCCCAGCGTCCAAAAGCGTCCCGGAGCGTCCAAGCGTCCAGCGTCCAAGCGTCCAGCGTCCGAGCGTCCAGCGTCCAAAGCGTCCTCGCGGTAGCGTCCTCTTAGCGTCCAGCGTCCAGCGTCCTGAGAAGCGTCCAGCGTCCAAGCGTCCAGTTGAGCGTCCAGCTAGCGTCCAGCGTCCGGGCAGAGCAAGCGTCCTACAGCGTCCGGATTGAGCGTCCATAGCGTCCCTTTCGTGTAGTTTGAGCGTCCTAGCGTCCAGCGTCCGAGCGTCCAAGCGTCCGAGCGTCCATAAGCGTCCCAAGCGTCCGGAAGCGTGACGGTAGCGTCCGTCGAGCGTCCAGACAGCGTCCAGCGTCCGGAGCGTCCGAGCGTCCAGCGTCCCCGGGTACATGTAGCGTCCGTGCCTAGCGTCCCGAGCGTCCAGCGTCCAGCGTCCGGCAGCGTCCAAGCGTCCAAGCGTCCAGCGTCCTCACTAAGCGTCCAGCGTCCGAGCGTCCAGCGTCCGAGAGCGTCCGAGCGTCCAGATGGAATATAGCGTCCGTAGCGTCCGGGCTCTTGAGCGTCCAATAGGAAACAAGCGTCCGAAGCGTCCAAGCGTCCAGTAGTCCAGCGTCCTAGCGTCCAGCGTCCCTTAGCGTCCTAGCGTCCGAGCGTCCGGAATTAAGAGCGTCCAGAAGCGTCCACTGGCGGTGGCAGCGTCCTAGCGTCCAGCGTCCAGCGTCCAGAGCGTCCGATTCAGCGTCCGAAGAGCGTCCGACAGCGTCCTGTGAGTGCCTAAGCGTCCGCTTAGCGTCCGTAGCGTCCTAGCGTCCATCAGCGTCCAGATAATTTAGCGTCCAGCGTCCATAGCGTCCTCAGCGTCCCAGCGTCCACGTCTTGTTAGCGTCCCCAGCGTCCCTCATTCTAGCGTCCGAAGCGTCCGGAGCGTCCAAGCGTCCTTCCAAATTAAGCGTCCTCCAGCGTCCAGCGAGCGTCCGTCTGGTAGCGTCCTGAGGAGCGTCCAGCGTCCACAGAGCGTCCGCGTTGTGAGCGTCCGAGCGTCCAGCGTCCAGCGTCCATCGAGCGTCCGTCAGGCGCCCCAGGCTCAGCGTCCAGCGTCCGAGCGTCCAGCGTCCAGCGTCCGAAAGCGTCCAGCGTCCAGCGTCCGAGGTGGGGAGCGTCCAGCGTCCTAAAGTAAAGCGTCCTAGCGTCCAGCGTCCGGAAGCGTCCGTTGAGCGTCCAGCGTCCCCGAGCGTCCCCAGCGTCCGAGCGTCCTGGCTTACTAAGCGTCCGAGCGTCCAGAACAGCGTCCCTAGCGTCCTGAGCGTCCCTGAATAGCGTCCAGTTAGCGTCCAGCGTCCCGATCAAGCGTCCGCAAAGGAGCGTCCTAGCGTCCAGCGTCCGTCAGCGTCCGGTAAAGCGTCCCTATTCAGCGTCCGCTCAGCGTCCCTAAGCGTCCAGTAGCGTCCAAAGCGTCCAAGAGCGTCCAGCGTCCCTACTGAATAAGCGTCCAGCGTCCAGCGTCCGATAGCGTCCTCGAGCGTCCATGGTGAGCGTCCAGCGTCCAGCGTCCCACCGTATGGAGCGTCCGGACAGCGTCCAGCGTCCAGCGTCCTAGCGTCCAGCGTCCAGCGTCCGCAGCGTCCAGCGTCCCAGCGTCCGTAAAGCGTCCAGCGTCCAGCGTCCTGAACTTAGCGTCCGAGCGTCCTCAAGCGTCCAGCGTCCAGCGTCCTAGCGTCCGGAGCGTCCTAGCGTCCGTAGCGTCCAGCGTCCAGCGTCCAGCGTCCTTAGCGTCCAGCGTCCCCATAGCGTCCCATAGCGTCCAGCGTCCCAGCGTCCTTTGTCCACTAGCGTCCTCGCGGCTTGCTTAGCGTCCTGAGCGTCCAGCGTCCAGCGTCCAGCGTCCGAGTTTCCCTTCAACGCACAGCGTCCTGCTAGCGTCCGAGCGTCCCAAGCGTCCCAGCGTCCCGTAGCGTCCGAGCGTCCGAAGCGTCCCTATCCAGCGTCCTGCATAGCGTCCAGCGTCCAGCGTCCCTTTTGCAGCGTCCGCTTGCGGCATATGGGTAGCGTCCAGAGCGTCCCCCTAGCGTCCTTGTAGCGTCCAAAGCGTCCCAAGCGTCCAGCGTCCGACAGCGTCCTAAGCGTCCCGAAAGCGTCCAGCGTCCAGCGTCCTCTAGCGTCCCAGCGTCCAGCGTCCAATGGGAAGCGTCCGTCCTAGCGTCCAGCGTCCCTGGAGCGTCCAGCGTCCTAGCGTCCCAGCAGCGTCCACTAAGCGAGCGTCCTAGCGTCCCCAGCGTCCCGTCAAGCGTCCAGCGTCCTAGCGTCCTAGCGTCCCCAGCGTCCCGGAGCGTCCGAGCGTCCCAGCGTCCTAGCGTCCAGAAGCGTCCAGCGTCCAAGCGTCCGCCCAGCGTCCAGCGTCCCGTAGCGTCCGGACACTAGCGTCCGGGAACAACAGGTGAGCGTCCAGCGTCCAGCGTCCCAGCGTCCTCGTTAGCGTCCAGCGTCCCAGCGTCCCCAGCGTCCAAGCGTCCGTTGCTGGATAGCGTCCAGCGTCCAGCGTCCAGAGCGTCCTAGGCCAGCGTCCGGAACGGTGGACAACAAGCGTCCACTTGAGCGTCCAGCGTCCAGAAGCGTCCAAGCGTCCAGCGTCCAGCGTCCCTGAGCGTCCAGCGTCCGTAGCGTCCTAGCGTCCTCAGCGTCCAGTTTAGCGTCCTAGCGTCCTCAAGCGTCCAGCGTCCGAGCGTCCAGCGTCCAGTTAGCGTCCCCCAGCGTCCAGCGTCCTTGCTGTAGCGTCCAAGCGTCCAGCGTCCGAGCGTCCCAAGCGTCCGAGCGTCCAGCGTCCTGAGAGCGTCCGAGCCGAAGCGTCCTGAGCGTCCGATTGAACCAGCGTCCAAAAGCGTCCGCACGGCAGCGTCCAGCGTCCTATCGTCTCACGCAGTAACTAGCGTCCGTTAGCGTCCAGCGTCCAGCGTCCGAGCGTCCAAAAGAGCGTCCATTTGGAGCGTCCAGACCGAGCGTCCAGCGTCCAGCGTCCGAAGCGTCCAGCGTCCGCCAAACTGAGCGTCCGAGCGTCCCCAGCGTCCAGCGTCCAGCGTCCAAGCGTCCTAGCGTCCACAGCGTCCAGCGTCCGATCAGCGTCCCAGCGTCCAGCGTCCCAGGAGCGTCCCTGCTGACAAGCGTCCTAGCGTCCGAAGCGTCCAGAGCGTCCAGCGTCCAAAAGCGTCCAAAAGCGTCCAGCGTCCTCCAGCGTCCCAGCGTCCGGAAGCGTCCAGCGTCCCAAGAGGTCCGAGGGCAAAGCGTCCAGCGTCCTAGCGTCCAGCGTCCTGGAGCGTCCAGCGTCCAGCGTCCCAAGCGTCCTTGAGCGTCCAGCGTCCTAGCGTCCGAGTAGCGTCCATCGCAGCGTCCAGCGTCCTAGCGTCCAGCGTCCAGCGTCCAGAGCGTCCAAGCGTCCGACAAAGCGTCCAGCGTCCATAGCGTCCAGCGTCCCTAGCGTCCAGCGTCCAGCGTCCAGCGTCCAGCGTCCTAGCGTCCAGCGTCCGGGCCTGTAGCGTCCAGCGTCCAGCGTCCAGCGTCCATAGCGTCCTTGGAGCGTCCAGCGTCCTGAAGCGTCCAAGCGTCCCGAGCGTCCCAGCGTCCTGAGCGTCCGATGTAGCGTCCAGCGTCCCCCCTAAACCTCTAGAGCGTCCTATCAGCGTCCTATGCGTCAGCGTCCAGCGTCCCGGCAGCGTCCCGAGCGTCCGAGCGTCCACCGTTATAGCGTCCAGCGTCCCAGCGTCCTGCCTCATAGCGTCCAGCGTCCTTAGCGTCCAAGCGTCCAGCGTCCAAGCGTCCGCAAGCGTCCTCTAGCGTCCATGAAATAGCGTCCAGCGTCCACAGCGTCCAGCGTCCTCCAGCGTCCGGGAGCGTCCAGAAAAAAGCGTCCCTAGCGTCCGCACATAGCGTCCCACAATTGTCAGCGTCCGGTCAGTTATAGCGTCCGCAGCGTCCACAGCGTCCGGAGCGTCCAGCAGCGTCCGTAGCGTCCAGCGTCCAACCAGCGTCCGCAAGCGTCCAGCGTCCGAAGCCCTAGCGTCCAGCGTCCCGAAGTAGCGTCCAGCGTCCCAGCGTCCCTTCAGCGTCCCCAGCGTCCGTTAGCGTCCCCAGCGTCCAGCGTCCGATCAGCGTCCTCAGCAGCGTCCGAGCGTCCAGAGAAAAAGCGTCCCCTACTAACCAGCGTCCTAGCGTCCGAGCGTCCAGCGTCCACCCATAGCGTCCTATCCCAGCGTCCAAGCGTCCTAGCGTCCTAGCGTCCCAAGCGTCCGAGCGTCCAGCGTCCTGAGCGTCCCCTCCTTGCTAGCGTCCTGCGGCAAGCGTCCTGCAGCGTCCTAGCGTCCGAGCGTCCTGCTGTAAGCGTCCCAGCGTCCGTAGCGTCCAAGCGTCCTTAAGCGTCCAGGGTTCGAAGCGTCCTCAAGGTGTAGCGTCCCTCAGCGTCCATACAGCGTCCCAAGCGTCCATCACAGCGTCCCACGATAGCGTCCAGCGTCCTACAAAGCGTCCTTAGCGTCCAAAAGCGTCCTAGCGTCCCGGAGCGTCCGAGAAGCGTCCGGGAGCGTCCAGCGTCCACAGTGAGCGTCCAGCGTCCCAGCGTCCCTACACAGCGTCCAGCGTCCAGCGTCCTTGATAGCGTCCGCCGAGCGTCCGTGAGCGTCCAGAGCGTCCCTTGAGCGTCCAAGCGTCCGTTAGCGTCCGTCACCCAGCGTCCAGCGTCCAGCGTCCAGCGTCCCAGCGTCCAGCGTCCCAAGCGTCCTCATAACGTTAGCGTCCAGCAGCGTCCAGCGTCCACTATGGAGCGTCCAAGCGTCCGCAGCGTCCAGAACTTTAGCGTCCAGCGTCCAGCGTCCAGCGTCCAGCGTCCCACAGCGTCCTAGCGTCCGGGCGGAGCGTCCCAGCGTCCAGCGTCCTACGAAGGTTAAGAAGCGTCCTCCATTAGCGTCCGATCATAGAGCGAGCGTCCAACAGCGTCCAGCGTCCAGCGTCCTCGATAGCGTCCAGCGTCCTGAGCGTCCTTAGCGTCCCATAGCGTCCCGGTGGAGCGTCCAGCGTCCCAAAGCGTCCAGCGTCCTAGCGTCCATAACTGCGCTGCAGCGTCCCAGCGTCCTCTCTAGCGTCCGTAGCGTCCCCTTAGCGTCCAGCGTCCTTAGCGTCCCAGCGTCCAGCGTCCATAGCGTCCAGCGTCCGTTTTATATAGCGTCCCAGCGTCCAGCGTCCGAGCGTCCAGCGTCCAGCGTCCAGCGTCCTTTAGCGTCCCAGCGTCCATGATAGCGTCCAGCGTCCAAGCGTCCAGCGTCCAGCGTCCGGATTTCACACATATAGAGCGTCCGAGAGGTAAAGCGTCCGCAGCGTCCCATTGCAGCGTCCAGCGTCCGAAAGCGTCCCAGCGTCCAGCGTCCCTGAGCGTCCAAGCGTCCAAGCGTCCAGCGTCCAAGTCAGCGTCCGAAGCGTCCTACTAGCGTCCAGCGTCCTAGCGTCCGAGCGTCCAGCGTCCGCAGCGTCCAGCGTCCCCTAGCGTCCAGCGTCCAGCGTCCAAAGCGTCCGGCAAGCGTCCGAGCGTCCAGCGTCCAAGCGTCCAGCGTCC" )
import sys
sys.exit(0)

#print (HammingDistance("GGGCCGTTGGT", "GGACCGTTGAC"))
#print ApproximatePatternMatching("GAGG", "TTTAGAGCCTTCAGAGG", 2)
#print ReverseComplement("TTATCCACA")
#print ReverseComplement("GGATCCTGG")
#print ReverseComplement("GATCCCAGC")
#print MinimumSkew("CCATGGGCATCGGCCATACGC")
#print SymbolArray("AAAAGGGG", "A")
#print FrequentWords(bioText, 10)
#print PatternCount(bioPattern, bioText)
#print reverseComplement("GCTAGCT")
#import os.path
#with open(os.path.normpath("C:\Users\IBM_ADMIN\Downloads\lol.txt")) as f:
#    lines = f.read().splitlines() 
    
