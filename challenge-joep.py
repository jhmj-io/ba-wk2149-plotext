from csv import reader
from functools import reduce
from datetime import datetime
import plotext as plt

print("\nChallenge Junior Data Engineer week 49 - Joep Jaspars")

path = "challenge-ratings.csv"
limit = 9999

# --- generieke functies --- #

# --- dictionary omzetten naar een list --- #
def dict2list (d,l ): #=[]): # hmmm ?! bij hernoemde aanroep bestaat de l uit vorige aanroep nog en wordt aangevuld?!
    for r in d: l.append( {r: d[r]})
    return l

# --- sommeer de tellingen en sommeer de gewogen telling --- #
def asignmentsratingsstat(e):
    e["arcw"] = 0
    e["arc"] = 0
    for r in e[ list(e.keys())[0] ]:
        e["arcw"] += int(r) * e[ list(e.keys())[0] ] [r]
        e["arc"] += e[ list(e.keys())[0] ] [r]

    return e


# --- read csv into list of dictionaries --- #
def map_csv_row2dict  (d,r) :
    o = dict()
    for i, a in  enumerate(d):
        o[a] = r[i]
    return o

def map_csv_rows2list (path):

    l = list()
    with open(path) as f:
        rr  = reader( f, delimiter=',', quotechar='|' )
        d = next(rr)
        d.insert(0,"id")
        for i, r in enumerate( rr ):
            r.insert(0,i)
            l.append( map_csv_row2dict(d,r) )
            if i>=limit: break
    return l

ratings = map_csv_rows2list(path)

# --- tellen per opdracht, per rating --- #

def sumexerciserating ( a, y):

    if y["exercise"] not in a.keys() :
        a[y["exercise"]] = {} 

    if y["rating"] in a[y["exercise"]].keys():
        a[y["exercise"]] [y["rating"]] += 1
    else: 
        a[y["exercise"]] [y["rating"]] = 1

    return a

ratingsdict = reduce( sumexerciserating, ratings, {} )
ratingslist = dict2list(ratingsdict, [])
  

# --- sommeer tellingen over alle opdracht en alle ratings --- #
def sumgrand ( a, y):

    for r in y [ list(y.keys())[0] ]:
        a += y [ list(y.keys())[0] ][r]

    return a

ratingscount = reduce( sumgrand, ratingslist, 0 )

# Totaal aantal ratings - 1 ster
print("\n1 Ratings aantal")
print("  »","Totaal:", ratingscount)




# Laat per opdracht zien hoeveel ratings de opdracht heeft en geef de namen van de opdrachten met een gemiddelde rating lager dan 3 - 2 sterren

# --- bereken statistieken per opdracht:  som telling ratings en gemiddelde --- #
assignmentsratings = list( map( asignmentsratingsstat, ratingslist))

print("\n2 Ratings per opdracht")

for a in assignmentsratings:

    print  ( "  »",list(a.keys())[0], "-","aantal:" + str(a["arc"]) ,  "LAGER DAN 3 GEMIDDELD"  if a["arcw"]//a["arc"] < 3 else ""  )




# --- filter opdracht "Flex met boxen" --- #
ratingsfiltered = list( filter( (lambda x : x['exercise'] == "Flex met boxen") , ratings ) )


# --- tellen per maand, per rating --- #
def sumexerciseratingmonth ( a, y):
    d = datetime.strptime(y['date'], '%Y-%m-%d')
    yearmonth = str(d.year)+("0"+str(d.month))[-2:]

    if yearmonth not in a.keys() :
        a[ yearmonth ] = {} 

    if y["rating"] in a[ yearmonth ].keys():
        a[yearmonth] [y["rating"]] += 1
    else: 
        a[yearmonth] [y["rating"]] = 1

    return a

ratingsdictfiltered = reduce( sumexerciseratingmonth, ratingsfiltered, {} )
ratingslistfiltered = dict2list( ratingsdictfiltered, [] ) 


# --- bereken statistieken per maand:  som telling ratings en gemiddelde --- #
assignmentsratingsfiltered = list( map( asignmentsratingsstat, ratingslistfiltered ))


# --- sorteer op YYYYMM --- #
assignmentsratingsfiltered.sort(key = lambda r: list(r.keys())[0] )


# Op 1 mei 2021 is de opdracht Flex met boxen herzien, heeft dat geleid tot betere ratings - 3 sterren #
print("\n3 Ratings opdracht 'Flex met boxen' per maand")

for a in assignmentsratingsfiltered:

    print  ( "  »", list(a.keys())[0], "-","aantal:", str(a["arc"])+"," , "gemiddeld:", a["arcw"]//a["arc"]   )

print("\n")


# --- prepare lists for plot --- #
months = list( map( lambda m: list(m.keys())[0], assignmentsratingsfiltered ))
monthsaverage = list( map( lambda m: m["arcw"]//m["arc"] , assignmentsratingsfiltered ))

# Data traject: Maak een grafiek waarin je laat zien wat de invloed was van de herzage. - Bonus #

print("\n4 Bonus opdracht 'Flex met boxen' per maand - grafiek\n")

plt.bar(months, monthsaverage)

plt.plot_size(width=90, height=30)
plt.title("Bonus - Ratings opdracht 'Flex met boxen' per maand")
plt.show()

print("\n--- fin ---")
