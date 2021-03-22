class calc3dRange:
    radius = 0
    area = []
    areaType = ""

    def __init__(self,area,size,toWrite = False):
        self.areaType = area
        if self.areaType == "Emanation" or self.areaType == "FlyUp" or self.areaType == "FlyDown" or self.areaType == "AirWalk":
            self.emanationInit(size)
        elif self.areaType == "Burst":
            self.burstInit(size)

        self.calcEmanationBurst()
        if toWrite:
            self.writeCsv()
    
    def writeCsv(self):
        with open("areas3d/" + self.areaType + str(5*self.radius) + ".csv","w+") as csvFile:
            for i in range(len(self.area)):
                for j in range(len(self.area)):
                    toWrite = str(self.area[i][j]) if self.area[i][j] != None else "-"
                    csvFile.write(toWrite)

                    if j + 1 < len(self.area):
                        csvFile.write(",")
                    else:
                        csvFile.write("\n")

    def burstInit(self,area):
        self.radius = area//5
        self.area = [[[None,None,None] for j in range(2*self.radius)] for i in range(2*self.radius)]
        for i in range(self.radius):
            for j in range(self.radius):
                self.area[i][j] = [abs(i - self.radius),abs(j - self.radius),0]

        for i in range(2*self.radius):
            for j in range(2*self.radius):
                if i < self.radius and j < self.radius:
                    continue
                
                iPos = i if i < self.radius else 2*self.radius - i - 1 
                jPos = j if j < self.radius else 2*self.radius - j - 1
                
                for k in range(3):
                    self.area[i][j][k] = self.area[iPos][jPos][k]

    def emanationInit(self,area):
        self.radius = area//5
        self.area = [[[abs(i - self.radius),abs(j - self.radius),0] for j in range(2*self.radius + 1)] for i in range(2*self.radius + 1)]

    def calcEmanationBurst(self):
        for i in range(len(self.area)):
            for j in range(len(self.area)):
                self.area[i][j] = self.findCoord(self.area[i][j],self.radius)

                if self.area[i][j][2] == None:
                    self.area[i][j] = None
                else:
                    self.area[i][j] = (self.area[i][j][2] + 1)* 5 if self.areaType == "Burst" else self.area[i][j][2] * 5



    def findCoord(self,posBase,maxDist):
        pos = [posBase[0],posBase[1],posBase[2]]
        totDist = self.calcDist(pos)
        if totDist == None or totDist > maxDist:
            pos[2] = None
            return pos
        
        while(totDist <= maxDist):
            pos[2] += 1
            totDist = self.calcDist(pos)
        pos[2] -= 1

        return pos

    def calcDist(self,posBase):
        pos = [posBase[0],posBase[1],posBase[2]]
        totDist = 0
        if self.areaType == "FlyUp":
            flyMod = pos[2]
        elif self.areaType == "FlyDown":
            flyMod = pos[2]//2
            pos[2] = 0 if pos[2] % 2 == 0 else 1
        else:
            flyMod = 0

        orderedPos = sorted(pos)

        if self.areaType == "AirWalk" and (pos[0]+pos[1]) < pos[2]:
            flyDif = pos[2] - (pos[1] + pos[0])
            
            while(orderedPos[0] < orderedPos[1] and flyDif > 0):
                orderedPos[0] += 1
                flyDif -= 1

            orderedPos[0] += flyDif//2 if flyDif % 2 == 0 else flyDif//2 + 1
            orderedPos[1] += flyDif//2
            if orderedPos[0] > orderedPos[1]:
                auxPos = orderedPos[0]
                orderedPos[0] = orderedPos[1]
                orderedPos[1] = auxPos


        while len(orderedPos) > 0 and orderedPos[0] == 0 :
            del orderedPos[0]

        if len(orderedPos) == 0:
            return 0



        if len(orderedPos) == 1:       
            totDist += orderedPos[0] + flyMod

            return totDist

        if len(orderedPos) == 3:

            totDist += 1.5*orderedPos[0]

            toRemove = orderedPos[0]
            while(orderedPos[1] < orderedPos[2] and toRemove > 0):
                toRemove -= 1
                orderedPos[2] -= 1

            orderedPos[1] -= toRemove//2
            orderedPos[2] -= toRemove//2 if toRemove % 2 == 0 else toRemove//2 + 1
            if orderedPos[1] > orderedPos[2]:
                auxOrder = orderedPos[1]
                orderedPos[1] = orderedPos[2]
                orderedPos[2] = auxOrder
            
            del orderedPos[0]

        totDist += (1.5*orderedPos[0]) + (orderedPos[1] - orderedPos[0]) + flyMod

        return int(totDist)
    
    def printFullArea(self):
        for i in self.area:
            for j in i:
                print(str(j),end="\t")
            print("\n")
        print("")

    def printAreaHeight(self,height,scrap=True):
        areaSlice = []
        for i in self.area:
            areaSlice.append([])
            for j in i:
                if j != None and j >= height:
                    areaSlice[-1].append("X")
                else:
                    areaSlice[-1].append(None)
        if len(self.area) % 2 == 1:
            
            print("Encontrado = "+str(self.radius))
            areaSlice[self.radius][self.radius] = "O"

        if scrap:
            while(len(areaSlice) > 1 and areaSlice[0] == len(areaSlice[0])*[None]):
                for i in range(len(areaSlice[0])):
                    del areaSlice[i][0]
                    del areaSlice[i][-1]
                del areaSlice[0]
                del areaSlice[-1]
        
        if areaSlice != [[None]]:
            for i in areaSlice:
                for j in i:
                    print(str(j),end="\t")
                print("\n")
            print("")
        else:
            print("Invalid")


areaTypes = ["Emanation","Burst","FlyUp","FlyDown","AirWalk"]

for i in areaTypes:
    for j in range(5,125,5):
        aux = calc3dRange(i,j,True)