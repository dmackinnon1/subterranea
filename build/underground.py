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

# functions that help extract sets from goal set
def dayAlone(day):
    statements = []
    for i in time:
        for j in time:
            statements.append([day, i, j])
    return statements
 
def dayAloneStatement(day):
    return "It is " + day + "."

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
    return "I am a " + day + "-knight."

def otherAloneStatement(day):
    return "The other person is a " + day + "-knight."

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
    return "I am a " + self + "-knight, and it is " + day + "."

def oppositeDayStatement(day):
    return "It is not " + opposite(day) +"."


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
    return "The other persion is a " + other + "-knight, and it is " + day + "."

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
    return "I am a " + self + "-knight, and the other persion is a " + other + "-knight."

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
        person1Statements.append({'statement': selfAloneStatement(d), 'state': selfAlone(1,p)})
        person2Statements.append({'statement': selfAloneStatement(d), 'state': selfAlone(2,p)})
        person1Statements.append({'statement': oppositeDayStatement(d), 'state': dayAlone(d)})
        person2Statements.append({'statement': oppositeDayStatement(d), 'state': dayAlone(d)})

# puzzle json
def jsonForPuzzle(puzzle):
    json = '{"bro0": "' + puzzle['bro0_text'] + '", ' 
    json += ' "bro1": "' + puzzle['bro1_text'] + '", '  
    json += ' "bro0_name": "' + puzzle['solution'][0][0] + '", '  
    json += ' "bro1_name": "' + puzzle['solution'][1][0] + '", '  
    json += ' "bro0_card": "' + puzzle['solution'][0][1] + '", '  
    json += ' "bro1_card": "' + puzzle['solution'][1][1] + '", '     
    json += ' "solution": "' + str(puzzle['solution']) + '", '
    json += ' "explanation": "' + puzzle['explanation'] + '", '  
    json += ' "id": "' + str(puzzle['id']) + '"}' + '\n'
    return json

# generate puzzles

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
            puzzles.append(p)
print('We generated ' + str(solutionCount) + " puzzles.")


#json output
def jsonForPuzzle(p):
    json = '{"time":"' + p['time'] + '",' 
    json += '"person1":"' + p['person1'] + '",'
    json += '"person2":"' + p['person2'] + '",'
    json += '"person1_type":"' + p['person1_type'] + '",'
    json += '"person2_type":"' + p['person2_type'] + '",'
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
