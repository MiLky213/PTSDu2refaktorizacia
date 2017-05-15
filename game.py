from random import randint

class player:
    def __init__(self, number):
        self.number = number
        self.order = 1
        self.position = dict()
        self.d = dict()
        self.setPosition()
        self.makeDict()
        self.counter = 0

    def setPosition(self):           
        self.position["1"] = (10,0), "h"
        self.position["2"] = (10,1), "h"
        self.position["3"] = (9,0), "h"
        self.position["4"] = (9,1), "h"
        self.position["A"] = (10,10), "h"
        self.position["B"] = (10,9), "h"
        self.position["C"] = (9,10), "h"
        self.position["D"] = (9,9), "h"

        if self.number >= 3:
            self.position["E"] = (0,0), "h"
            self.position["F"] = (0,1), "h"
            self.position["G"] = (1,0), "h"
            self.position["H"] = (1,1), "h"
        if self.number >= 4:
            self.position["I"] = (0,9), "h"
            self.position["J"] = (0,10), "h"
            self.position["K"] = (1,9), "h"
            self.position["L"] = (1,10), "h"

class game(player):

    def __init__(self, players = 2):
        if players > 4:
            print("Privela hracov, max su 4")
            return None

        # hracia plocha
        self.place = [
            (10,4),(9,4),(8,4),(7,4),(6,4),(6,3),(6,2),(6,1),(6,0),(5,0),
            (4,0),(4,1),(4,2),(4,3),(4,4),(3,4),(2,4),(1,4),(0,4),(0,5),
            (0,6),(1,6),(2,6),(3,6),(4,6),(4,7),(4,8),(4,9),(4,10),(5,10),
            (6,10),(6,9),(6,8),(6,7),(6,6),(7,6),(8,6),(9,6),(10,6),(10,5)
        ]

        # oznacenia figuriek hracov
        self.p = [
            ["1", "2", "3", "4"],
            ["A", "B", "C", "D"],
            ["E", "F", "G", "H"],
            ["I", "J", "K", "L"]
        ]
        
        self.players = players
        self.gameMap = []
        self.loadMap()
        super().__init__(players)
        self.turn = 0
        self.numMove = 0

    def loadMap(self):
        self.gameMap = []
        with open('map.txt') as file:
            for line in file:
                foo = []
                for char in line:
                    if char == ',':
                        foo.append(" ")
                    elif char != '\n':
                        foo.append(char)
                self.gameMap.append(foo)

    def __str__(self):
        s = ""
        arr = [self.position[name][0] for name in self.position]

        # vykreslenie hracej plochy
        for i in range(len(self.gameMap)):
            for j in range(len(self.gameMap[i])):
                if (i,j) in arr:
                    for name in self.position:
                        if self.position[name][0] == (i,j):
                            s += name + " "
                else:
                    s += self.gameMap[i][j] + " "
            s += "\n"
        return s

    def throwCube(self):
        self.numMove = randint(1,6)
        return self.numMove

    def checkPlayer(self):
        return self.order

    def nextPlayer(self):
        if self.players in [2,3,4]:
            self.order += 1
            if self.order == self.players+1:
                self.order = 1

    def checkAllHome(self, player):
        for i in self.p[player-1]:
            if self.position[i][1] != "h":
                return False
        return True

    def checkHome(self, player):
        s = ""
        for i in self.p[player-1]:
            if self.position[i][1] != "h":
                s += i+", "
        return s[:-2]

    def makeDict(self):
        for i in range(1, 41):
            self.d[i] = self.place[i-1]

    def newFromHome(self, player, cube):
        a = input("Vyber si jedneho z domceka: ")
        if ( not self.checkCorrectPLayer(player, a)):
            print("Zly vyber, skus to znova...")
            self.newFromHome(player, cube)
            return
        x = [1, 39, 19, 21]
        self.position[a] = (self.d[ x[player-1] ][0], self.d[ x[player-1] ][1]), "n"
        
        self.counter = 0
        print(g)
        self.nextPlayer()

    def checkLose(self, player):
        for i in self.p[player-1]:
            if self.position[i][0] != (-1000,-1000):
                return False
        return True

    def move(self,player, cube):
        print("na vyber mas tycho hracov: " + self.checkHome(player))
        a = input("Vyber si jedneho: ")
        if ( not self.checkCorrectPLayer(player, a)):
            print("premrhal si svoje sance zlou figurkou! Ide dalsi")
            self.nextPlayer()
            return
        poz = self.position[a][0]
        it = list(self.d.keys())[list(self.d.values()).index(poz)]
        it = it + cube
        if (it > 40): it = it - 40
        self.position[a] = (self.d[it][0], self.d[it][1]), "n"
        for name in self.position:
            if ( name != a and self.position[name][0] == self.position[a][0] ):
                print("vyhodil si figurku: " + name)
                print("hrac s touto figurkou uz dalej nemoze hybat")
                self.position[name] = (-1000,-1000), "h"
                if(self.checkLose(player)):
                    print("Hrac s cislom " + str(player) + " prehral")
                    sys.exit(0)
                    return
        print(g)
        self.nextPlayer()

    def checkCorrectPLayer(self, player, s):
        if(player == 1):
            if (s in "1234"): return True
        if(player == 2):
            if (s in "ABCD"): return True
        if(player == 3):
            if (s in "EFGH"): return True
        if(player == 4):
            if (s in "IJKL"): return True

    def play(self):
        player = self.checkPlayer()
        cube = self.throwCube()
        if(self.counter == 3):
            print("Vycerpal si vsetky pokusy ide dalsi")
            self.nextPlayer()
            self.counter = 0
            return
        print("Na rade je hrac " + str(player))
        print("Hrac hodil cislo:" + str(cube))
        if(cube != 6 and self.checkAllHome(player)):
            self.counter += 1
            print("Mas vsetkych v domceku a nehodil si cislo 6, otava ti: " + str(3- self.counter) + " pokusy")

        elif ( cube == 6 and self.checkAllHome(player)):
            self.newFromHome(player,cube)
        elif ( cube == 6 and not self.checkAllHome(player)):
            a = input("Hodil si cislo 6 chces pokracovat alebo dat novu figurku a/n: ")
            if ( a != "a" and a != "n" ):
                print("Vyber spravnu moznost!")
                a = input("Hodil si cislo 6 chces pokracovat alebo dat novu figurku a/n: ")
            if (a == "a"):
                print("Zvolil si novu figurku")
                self.newFromHome(player,cube)
            elif ( a == "n" ):
                self.move(player,cube)
        else:
            self.move(player,cube)


a = input("Zadaj pocet hracov (2-4): ")
if int(a) > 1 and int(a) < 5:
    g = game(int(a))
    print(g)
    g.play()
else:
    print("Zadal si zly pocet hracov...")

### Testovanie prebieha samotnym hranim hry...




