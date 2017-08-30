import random
import copy
import traceback
import threading
import math

turncount = 0
clear = "\n" * 100
debug = 0
thread1 = []
thread2 = []
thread3 = []
result1 = []
result2 = []
result3 = []
t1 = 0
t2 = 0
t3 = 0

def turn(board, symbol):
    try:
        global debug
        global turncount
        currentValues = []
        x = 0
        y = 0
        while x < 8:
            currentValues.append([])
            while y < 8:
                currentValues[x].append(getboard(board,x,y))
                y = y + 1
            x = x + 1
            y = 0
        enemySymbol = ""
        if symbol == "X": enemySymbol = "O"
        elif symbol == "O": enemySymbol = "X"
        sim = 7
        if sim + turncount >= 32:
            sim = 32 - turncount - 1
        b = simMoves(currentValues,symbol,enemySymbol,sim,1,0)
        print("Finished Turn",turncount)
        turncount = turncount + 1
        if turncount > 32: turncount = 0
        if debug == 1: input("Continue?")
        if debug == 1: print(clear)
        best = -9999
        for l in range(0,len(b)):
            if b[l].weighting > best:
                best = b[l].weighting
                x = b[l].x
                y = b[l].y
            elif b[l].weighting == best:
                if random.choice([0,1,2]) == 1:
                    x = b[l].x
                    y = b[l].y
        if getboard(board,x,y) == "X" or getboard(board,x,y) == "O":
            print("ERROR");
        if x > 7 or y > 7:
            print("ERROROVER")
            print(len(b))
        print(best,x,y)
        print(str(turncount) + " turn Finished")
        return (x,y)

    except:
        var = traceback.format_exc()
        print(var)
        return (0,0)

def simMoves(currentValues,symbol,enemySymbol,deep, first, thread):
    global thread1
    global thread2
    global thread3
    moves = []
    if thread != 0:
        first = 0
        if thread == 1:moves = thread1
        elif thread == 2:moves = thread2
    else: moves = makeTurn(currentValues,symbol)
    if first == 1:
        global result1
        global result2
        global result3
        global t1
        global t2
        global t3
        choices = []
        x = 0
        y = 0
        while x < 8:
            while y < 8:
                if currentValues[x][y] == "#":
                    choices.append([x,y])
                y = y + 1
            y = 0
            x = x + 1
        for i in range(0,len(choices)):
            found = 0
            for i2 in range(0,int(len(moves))):
                if moves[i2].x == choices[i][0]:
                    if moves[i2].y == choices[i][1]:
                        found = 1
            if found == 0:
                moves.append(Point(choices[i][0],choices[i][1],0))
        split = list(chunkIt(moves, 4))
        moves = split[0]
        thread1 = split[1]
        thread2 = split[2]
        thread3 = split[3]
        t1 = worker(copy.deepcopy(currentValues),symbol,enemySymbol,deep,1)
        t1.start()
        t2 = worker(copy.deepcopy(currentValues),symbol,enemySymbol,deep,2)
        t2.start()
        t3 = worker(copy.deepcopy(currentValues),symbol,enemySymbol,deep,3)
        t3.start()
    debug = 0

    i = 0

    while i < len(moves):
    #print("Move",i / 3,"|",moves[i],"|",moves[i+1],"|",moves[i+2]
        if deep > 0:
            newValues = copy.deepcopy(currentValues)
            newValues[moves[i].x][moves[i].y] = symbol
            corners = [0,0,1,1,0,7,1,6,7,0,6,1,7,7,6,6]
            i2 = 0
            while i2<len(corners):
                if newValues[corners[i2]][corners[i2+1]] !=symbol and newValues[corners[i2]][corners[i2+1]]!='#':
                    if moves[i].x==corners[i2+2] and moves[i].y==corners[i2+3]:
                        newValues[corners[i2]][corners[i2+1]] = symbol
                i2 = i2 + 4

            if debug == 1 : print("r")
            #Nach Rechts
            x = moves[i].x
            y = moves[i].y
            cha = []
            confirm = -1
            while x < 8:
                if newValues[x][y] == enemySymbol: cha.extend([x,y])
                elif newValues[x][y] == symbol:
                    confirm = 1
                    x = 8
                x = x + 1
            if confirm == 1 and len(cha)>0:
                newValues = change(newValues,cha, symbol)

            if debug == 1 : print("l")
            #Nach Links
            x = moves[i].x-1
            y = moves[i].y
            cha = []
            confirm = -1
            while x > -1:
                if newValues[x][y] == enemySymbol: cha.extend([x,y])
                elif newValues[x][y] == symbol:
                    confirm = 1
                    x = -20
                x = x - 1
            if confirm == 1 and len(cha)>0:
                newValues = change(newValues,cha, symbol)

            if debug == 1 : print("u")
            #Nach Unten
            x = moves[i].x
            y = moves[i].y+1
            cha = []
            confirm = -1
            while y < 8:
                if newValues[x][y] == enemySymbol: cha.extend([x,y])
                elif newValues[x][y] == symbol:
                    confirm = 1
                    y = 8
                y = y + 1
            if confirm == 1 and len(cha)>0:
                newValues = change(newValues,cha, symbol)

            if debug == 1 : print("o")
            #Nach Oben
            x = moves[i].x
            y = moves[i].y-1
            cha = []
            confirm = -1
            while y > -1:
                if newValues[x][y] == enemySymbol: cha.extend([x,y])
                elif newValues[x][y] == symbol:
                    confirm = 1
                    y = -8
                y = y - 1
            if confirm == 1 and len(cha)>0:
                newValues = change(newValues,cha, symbol)

            eW = simMoves(newValues,enemySymbol,symbol,deep-1,0,0)
            all = 0
            highest = -999
            lowest = 999
            for l in range(0,int(len(eW))):
                if eW[l].weighting > highest:
                    highest = eW[l].weighting
                if eW[l].weighting < lowest:
                    lowest = eW[l].weighting
                all = all + eW[l].weighting
            all-= lowest
            all+= highest
            w = all / float(len(eW))
            moves[i].weighting = moves[i].weighting - w
        i = i + 1
    if thread != 0:
        if thread == 1:
            result1 = moves
            print("Second Thread finished")
        elif thread == 2:
            result2 = moves
            print("Third Thread finished")
        elif thread == 3:
            result3 = moves
            print("Fourth Thread finished")
    elif thread == 0 and first == 1:
        print("Main finished")
        t1.join(60)
        t2.join(30)
        t3.join(20)
        moves.extend(result1)
        moves.extend(result2)
        moves.extend(result3)
    return moves

def change(values,change, symbol):
    i = 0
    while i * 2 < len(change):
        values[change[i]][change[i+1]] = symbol
        i = i + 2
    return values

def makeTurn(currentValues,symbol):
    corners = [0,0,1,1,0,7,1,6,7,0,6,1,7,7,6,6]
    i = 0

    possible = []

    while i<len(corners):
        if currentValues[corners[i]][corners[i+1]] !=symbol and currentValues[corners[i]][corners[i+1]]!='#':
            if currentValues[corners[i+2]][corners[i+3]] == '#': possible.append(Point(corners[i+2],corners[i+3],1))
        i = i + 4

    possible.extend(searchAll(currentValues, symbol))
    best = [Point(-1,-1,-1)]
    if len(possible) != 0:
        e = 0
        while e < len(possible):
            if possible[e].weighting > best[0].weighting:
                best = [Point(possible[e].x,possible[e].y,possible[e].weighting)]
            elif possible[e].weighting == best[0].weighting:
                best.append(Point(possible[e].x,possible[e].y,possible[e].weighting))
            e = e + 1
    if best[0].weighting > 0:
        return best

    choices = []
    x = 0
    y = 0
    while x < 8:
        while y < 8:
            if currentValues[x][y] == "#":
                choices.append([x,y])
            y = y + 1
        y = 0
        x = x + 1
    if len(choices) == 0:
        return [Point(0,0,0)]
    c = random.choice(choices)
    return [Point(c[0],c[1],0)]


def searchAll(currentValues, symbol):
    res = []
    hor = searchAllHor(currentValues, symbol)
    verts = searchAllVerts(currentValues, symbol)
#Search for Multiples in Verts
    for i in range(0,len(hor)):
        x = hor[i].x
        y = hor[i].y
        found = 0
        for i2 in range(0,len(verts)):
            if x == verts[i2].x:
                if y == verts[i2].y:
                    found = 1
                    wH = hor[i].weighting
                    wV = verts[i2].weighting
                    res.append(Point(x,y,wH+wV))
                    i2 = 9999
        if found == 0:
            res.append(Point(x,y,hor[i].weighting))
#Search for Multiples in Hor
    for i in range(0,len(verts)):
        x = verts[i].x
        y = verts[i].y
        found = 0
        for i2 in range(0,len(hor)):
            if x == hor[i2].x:
                if y == hor[i2].y:
                    found = 1
                    i2 = 9999
        if found == 0:
            res.append(Point(x,y,verts[i].weighting))

    if len(res) != 0:
        return res
    return Point(-1,-1,-1)

def searchAllVerts(currentValues, symbol):
    y = 0
    best = []
    while y < 8:
        r = searchVert(currentValues,y, symbol)
        if r[0].x != -1:
            e = 0
            while e < len(r):
                if r[e].x > 0:
                    best.append(r[e])
                e = e + 1
        y = y + 1
    if len(best) == 0:
        return [Point(-1,-1,-1)]
    return best

def searchVert(currentValues, y, symbol):
    x = 0
    values = [0,0,0,0,0,0,0,0]
    found = -1
    enemyFound = -1
    while x < 8:
        if currentValues[x][y] == "#": values[x] = 0
        elif currentValues[x][y] == symbol:
            values[x] = 1
            found = 1
        elif currentValues[x][y] != symbol:
            values[x] = -1
            enemyFound = 1
        x = x + 1
    if found == 1 and enemyFound == 1:
        results = []
        x2 = 0
        while x2 < 8:
            if values[x2] == 1:
                x3 = x2 - 1
                emptyFound = []
                enemysFound = 0
                while x3 >= 0:
                    if values[x3] == -1:
                        enemysFound = enemysFound + 1
                    elif values[x3] == 0 and enemysFound > 0:
                        emptyFound.append(Point(x3,y,enemysFound))
                        break
                    x3 = x3 - 1
                enemysFound = 0
                x3 = x2 + 1
                while x3 < 8:
                    if values[x3] == -1:
                        enemysFound = enemysFound + 1
                    elif values[x3] == 0 and enemysFound > 0:
                        emptyFound.append(Point(x3,y,enemysFound))
                        break
                    x3 = x3 + 1
                results.extend(emptyFound)
            x2 = x2 + 1
        if len(results) != 0:
            return results
    return [Point(-1,-1,-1)]

def searchAllHor(currentValues, symbol):
    x = 0
    best = []
    for x in range(0,8):
        r = searchHor(currentValues,x, symbol)
        if r[0] != -1:
            for e in range(0,len(r)):
                if r[e].weighting > 0:
                    best.append(Point(r[e].x,r[e].y,r[e].weighting))
    if len(best) == 0:
        return [Point(-1,-1,-1)]
    return best

def searchHor(currentValues, x, symbol):
    y = 0
    values = [0,0,0,0,0,0,0,0]
    found = -1
    enemyFound = -1
    while y < 8:
        if currentValues[x][y] == "#": values[y] = 0
        elif currentValues[x][y] == symbol:
            values[y] = 1
            found = 1
        elif currentValues[x][y] != symbol:
            values[y] = -1
            enemyFound = 1
        y = y + 1
    if found == 1 and enemyFound == 1:
        results = []
        y2 = 0
        while y2 < 8:
            if values[y2] == 1:
                y3 = y2 - 1
                emptyFound = []
                enemysFound = 0
                while y3 >= 0:
                    if values[y3] == -1:
                        enemysFound = enemysFound + 1
                    elif values[y3] == 0 and enemysFound > 0:
                        emptyFound.append(Point(x,y3,enemysFound))
                        break
                    y3 = y3 - 1
                enemysFound = 0
                y3 = y2 + 1
                while y3 < 8:
                    if values[y3] == -1:
                        enemysFound = enemysFound + 1
                    elif values[y3] == 0 and enemysFound > 0:
                        emptyFound.append(Point(x,y3,enemysFound))
                        break
                    y3 = y3 + 1
                results.extend(emptyFound)
            y2 = y2 + 1
        if len(results) != 0:
            return results
    return [Point(-1,-1,-1)]

def chunkIt(seq, num):
    avg = len(seq) / float(num)
    out = []
    last = 0.0

    while last < len(seq):
        out.append(seq[int(last):int(last + avg)])
        last += avg

    return out

class Point():
    def __init__(self,x,y,weighting):
        self.x = x
        self.y = y
        self.weighting = weighting

class worker (threading.Thread):
    def __init__(self, currentValues,symbol,enemySymbol,deep, thread):
        threading.Thread.__init__(self)
        self.currentValues = currentValues
        self.symbol = symbol
        self.enemySymbol = enemySymbol
        self.deep = deep
        self.thread = thread
    def run(self):
        simMoves(self.currentValues,self.symbol,self.enemySymbol,self.deep,0,self.thread)
