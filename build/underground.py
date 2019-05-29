#
# Script to generate valid puzzles for Subterranea
#

# Set up the 'goal' set - triples of 'day' or 'night'
# first entry: the time of day
# second entry: type of the first inhabitant
# third entry: type of the second inhabitant

import math
time = ['day', 'night']
options = []
for i in time:
    for j in time:
        for k in time:
            options.append([i,j,k])
            
def opposite(day):
    if day == 'day':
        return 'night'
    return 'day'

def truthValue(person, option):
    return option[0] == option[person]

def firstInhabitant(option):
    return truthValue(1,option)

def secondInhabitant(option):
    return truthValue(2, option)

#truth function for inhabitants - give the set of true possibilities from a given set
def inhabitantTruths(person, statements = options):
    truths = []
    for o in statements:
        if o[0] == o[person]:
            truths.append(o)
    return truths

#'false' function for inhabitants - give the set of false possibilities from a given set
def inhabitantLies(person, statement = options):
    lies = []
    for o in statement:
        if o[0] != o[person]:
            lies.append(o)
    return lies

def complement(s):
    comp = []
    for o in options:
        if (o[0]!=s[0] or o[1]!= s[1] or o[2]!=s[2]):
            comp.append(o)
    return comp

def reducedAdd(listOne, listTwo):
    reduced = [] + listTwo
    for l in listOne:
        if l not in listTwo:
            reduced.append(l)
    return reduced

def fullComplement(statements):
    comp = []
    for s in statements:
        comp = reducedAdd(comp, complement(s))
    for s in statements:
        if s in comp:
            comp.remove(s)
    return comp

def intersection(set1,set2):
    intersect = []
    for s in set1:
        if s in set2:
            intersect.append(s)
    return intersect

# statement generators
def dayAlone(day):
    statements = []
    for i in time:
        for j in time:
            statements.append([day, i, j])
    return statements
 
def dayAloneStatement(day):
    return "It is " + day 

def selfAlone(person, self):
    a = ['blank','blank','blank']
    a[0]= 'day'
    a[person] = self
    a[int(2 -math.floor(person/2) % 2)] = 'day';
    b = ['blank','blank','blank']
    b[0] = 'day'
    b[person] = self
    b[int(2 -math.floor(person/2) % 2)] = 'night';
    c = ['blank','blank','blank']
    c[0]= 'night'
    c[person] = self
    c[int(2 -math.floor(person/2) % 2)] = 'day';
    d = ['blank','blank','blank']
    d[0]= 'night'
    d[person] = self
    d[int(2 -math.floor(person/2) % 2)] = 'night';   
    return [a,b,c,d]
    
def selfAloneStatement(day):
    return "I am a " + day + "-knight"

def otherAloneStatement(day):
    return "The other person is a " + day + "-knight"

#the person is making a statement about themselves and the day
def selfAndDay(person, self, day):
    a = ['blank','blank','blank']
    a[0]= day
    a[person] = self
    a[int(2 -math.floor(person/2) % 2)] = 'day';
    b = ['blank','blank','blank']
    b[0] = day
    b[person] = self
    b[int(2 -math.floor(person/2) % 2)] = 'night';
    return [a,b]

def selfAndDayStatement(self, day):
    return "I am a " + self + "-knight, and it is " + day 

def oppositeDayStatement(day):
    return "It is not " + opposite(day) 


# the person is making a statement about the other and the day 
def otherAndDay(person, other, day):
    a = ['blank','blank','blank']
    a[0]= day
    a[person] = 'day'
    a[int(2 -math.floor(person/2) % 2)] = other;
    b = ['blank','blank','blank']
    b[0] = day
    b[person] = 'night'
    b[int(2 -math.floor(person/2) % 2)] = other;
    return [a,b]

def otherAndDayStatement(other, day):
    return "The other person is a " + other + "-knight, and it is " + day 

# the person is making a statement themselves and the other 
def otherAndSelf(person, self, other):
    a = ['blank','blank','blank']
    a[0]= 'day'
    a[person] = self
    a[int(2 -math.floor(person/2) % 2)] = other;
    b = ['blank','blank','blank']
    b[0] = 'night'
    b[person] = self
    b[int(2 -math.floor(person/2) % 2)] = other;
    return [a,b]

def otherAndSelfStatement(other, self):
    return "I am a " + self + "-knight, and the other person is a " + other + "-knight"

# combine all statements
person1Statements = []
person2Statements = []
for p in time:
    for d in time:        
        person1Statements.append({'statement': selfAndDayStatement(p,d), 'state': selfAndDay(1,p,d)})
        person1Statements.append({'statement': otherAndDayStatement(p,d), 'state': otherAndDay(1,p,d)})
        person1Statements.append({'statement': otherAndSelfStatement(p,d), 'state': otherAndSelf(1,p,d)})
        person2Statements.append({'statement': selfAndDayStatement(p,d), 'state': selfAndDay(2,p,d)})
        person2Statements.append({'statement': otherAndDayStatement(p,d), 'state': otherAndDay(2,p,d)})
        person2Statements.append({'statement': otherAndSelfStatement(p,d), 'state': otherAndSelf(2,p,d)})

for d in time:
        person1Statements.append({'statement': dayAloneStatement(d), 'state': dayAlone(d)})
        person2Statements.append({'statement': dayAloneStatement(d), 'state': dayAlone(d)})
        person1Statements.append({'statement': selfAloneStatement(d), 'state': selfAlone(1,d)})
        person2Statements.append({'statement': selfAloneStatement(d), 'state': selfAlone(2,d)})
        person1Statements.append({'statement': oppositeDayStatement(d), 'state': dayAlone(d)})
        person2Statements.append({'statement': oppositeDayStatement(d), 'state': dayAlone(d)})

# functions for generating and formatting the explanations
def inWords(option):
    s = "it is " + option[0] +", and the first person is a " + option[1] +"-knight" 
    s += " while the second person is a " + option[2] + "-knight"
    return s

def longInWords(options):
    s = "It could be that ";
    s+= inWords(options[0])
    for i in range(len(options)-1):
        s+=', or '
        s+= inWords(options[i+1])
    return s

def explain(i, st):
    position = 'first'
    if (i == 2):
        position = 'second'
    s = "When the " + position + " inhabitant says '" + st['statement'] +"'"   
    truthCount = len(inhabitantTruths(i, st['state']))
    if truthCount == 0 :
        s += ", they cannot be telling the truth. "
    elif truthCount == 1 :
        s += ", if they are telling the truth, there is one possibility: " + inWords(inhabitantTruths(i, st['state'])[0]) + ". "
    else :
        s += ", if they are telling the truth, there are " + str(truthCount) + " possibilities: "  
        s += longInWords(inhabitantTruths(i, st['state']))
        s += "."
    lieCount = len(inhabitantLies(i, fullComplement(st['state'])))
    if lieCount == 0 :
        s += "By making this statement, they cannot be lying. "
    elif lieCount == 1 :
        s += "There is only one way the could be lying: " + inWords(inhabitantLies(i, fullComplement(st['state']))[0]) + ". "
    else :
        s+= "There are " +str(lieCount) + " ways they could be lying: "
        s+= longInWords(inhabitantLies(i, fullComplement(st['state'])))
        s+= "."
    return s

def stateSolution(sol, p1, p2):
    s = "There is only one possibility from both statements: the first person is "
    if p1 :
        s += 'telling the truth'
    else:
        s += 'lying'
    s += " and the second person is "
    if p2 :
        s += 'telling the truth. '
    else:
        s += 'lying. '
    s += "It must be that " + inWords(sol) +"."
    return s


solutionCount = 0
puzzles = []
for s1 in person1Statements:
    for s2 in person2Statements:
        ts1 = inhabitantTruths(1, s1['state'])
        fs1 = inhabitantLies(1, fullComplement(s1['state']))
        allS1 = reducedAdd(ts1,fs1)
        ts2 = inhabitantTruths(2, s2['state'])
        fs2 = inhabitantLies(2, fullComplement(s2['state']))
        allS2 = reducedAdd(ts2,fs2)
        solution = intersection(allS1, allS2)
        if len(solution) ==1 :
            solutionCount = solutionCount +1
            p = {'time': solution[0][0]}
            p['person1'] = s1['statement']
            p['person2'] = s2['statement']
            p['id'] = solutionCount
            p['person1_type']= solution[0][1]
            p['person2_type']= solution[0][2]
            p['person1_explain'] = explain(1,s1)
            p['person2_explain'] = explain(2,s2)
            p['solution_explain'] = stateSolution(solution[0],truthValue(1, solution[0]),truthValue(2, solution[0]))
            puzzles.append(p)            

# json output
def jsonForPuzzle(p):
    json = '{"time":"' + p['time'] + '",' 
    json += '"person1":"' + p['person1'] + '",'
    json += '"person2":"' + p['person2'] + '",'
    json += '"person1_type":"' + p['person1_type'] + '",'
    json += '"person2_type":"' + p['person2_type'] + '",'
    json += '"person1_explain":"' + p['person1_explain'] + '",'
    json += '"person2_explain":"' + p['person2_explain'] + '",'
    json += '"solution_explain":"' + p['solution_explain'] + '",'
    json += '"id":"' + str(p['id']) + '"'
    json += "}"
    return json

# write out the puzzles
result = "["
first = True
for p in puzzles:
    if not first:
        result += ", \n"
    else:
        first = False
    result += jsonForPuzzle(p)
result += "]"
print("There were " + str(len(puzzles)) + " puzzles generated")

f = open("../data/underground.json","w")
f.write( result )
f.close()
