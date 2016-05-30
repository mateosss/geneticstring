import random
from time import time
startTime = time()
# TODO ERRORS cuando algun gen llega a 0 o 255 queda ahi para siempre
# TODO ERRORS siempre se mantienen las letras de los padres, nunca se van a generar nuevas letras, hacer el crossover por cada gen(letra) y no por cromosoma
# TODO ERRORS Hacer el script threadsafe, buscar puntos donde sea posible mejorar el rendimiento
#The God Word, to what the subject aspires to be
god = "pato"

#General Rules for fitness score
wordLengthMaxScore = 0.5
letterEqualityMaxScore = 0.5
godFitness = wordLengthMaxScore + letterEqualityMaxScore
wordLengthTolerance = 10

#Various settings
tolerance = 5 #round the subject fitness by this tolerance to compare with the god fitness
crossoverRate = 0.7 # This does not work as in normal GA, this sets the influence of the strongest parent to let its genes
mutationRate = 0.1
mutationLimit = 30 #The +- in which the gen will mutate if needed
pause = 10000 #Pause after X rouletes
rouleteNumber = 1


#The race population
population = []

def adanEva():
    # TODO hacer que los primeros especimenes se generen aleatoriamente
    """
    - This function generates the initial population
    - The subject object has to receive a list of strings with 8 bit formats example Subject(["01010000","11001100","01011111"]) or just a string like Subject("adan")
    """
    s1 = Subject("adan")
    s2 = Subject("eva")
    s3 = Subject("pedro")
    s4 = Subject("clementina")
    population.append(s1)
    population.append(s2)
    population.append(s3)
    population.append(s4)


def rouleteOfGod():# TODO always the half populations, is that what i want?
    global population, pause, rouleteNumber, tolerance, startTime

    orderedPopulation = rollTheRoulete(True)
    crossovers = []

    # Selecting all the population (ordered by fitScore) to crossover
    for i in range(0,len(population)/2,2):
        crossovers.append(crossover(orderedPopulation[i], orderedPopulation[i+1]))

    # Making the crossover
    for cross in crossovers:
        firstSon = cross[2][0]
        secondSon = cross[2][1]

        population.append(firstSon)
        population.append(secondSon)

        # Check if the subject is the final answer
        theSonOfGod = False
        if tolerance != 0:
            if round(firstSon.fitScore,tolerance) == round(godFitness,tolerance):
                theSonOfGod = firstSon
            if round(secondSon.fitScore,tolerance) == round(godFitness,tolerance):
                theSonOfGod = secondSon
        else:
            if firstSon.fitScore == godFitness:
                theSonOfGod = firstSon
            if secondSon.fitScore == godFitness:
                theSonOfGod = secondSon

        # If it is
        if theSonOfGod != False:
            print("")
            print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
            print("THIS IS MY REAL SON, THE FINAL EVOLUTION, THIS IS ME")
            print(theSonOfGod.fitScore)
            print(theSonOfGod)
            elapsedTime = time() - startTime
            print("Done. In "+ str(rouleteNumber) + " Generations. In " + str(elapsedTime) + " Seconds.")
            print("")
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
            exit()
        # print("\t\t------------------")

    # Killing the weakests
    applyDeath(2,False)

    rouleteNumber += 1
    if pause != 0 and rouleteNumber%pause == 0:
        # Debug labors
        scores = []
        print("Population: "),
        for i in population:
            scores.append(i.fitScore)
            print("| "+i.__str__()+" "),
        print()
        print("AVG - " + str(round(sum(scores)/len(scores),tolerance)))
        print("pause...")
        # time.sleep(3)
    # time.sleep(1)


def crossover(c1, c2, sonsCount = 2):
    """
    - Parameters: stronger parent, weaker parent, quantity of childs
    - The first parent is considered the more evoluted, so it has 70 percent of chance for every character of use his genes insted of the other parent
    - The crossover is made by comparing the two parents letters and length, if the sons are equal to the parents they are deleted and reprocessed
    - The large of the word is determined by: the promedy of the two parents length plus a special random int
    - The characters are determined by: The total range to iterate is determined by the largest parent, for every letter the stronger parent has 70 percent
        of chances of let its genes (his letter), the weakest has 30 percent.
        - The characters in which one parent doesn't have characters to give
    - Return: stronger parent, weakest parent , List of childs
    """
    global crossoverRate, mutationRate, tolerance, godFitness, population, wordLengthTolerance
    parent1 = c1.value
    parent2 = c2.value
    if len(parent1) >= len(parent2):
        maxRange = len(parent1)
        minRange = len(parent2)
    else:
        maxRange = len(parent2)
        minRange = len(parent1)

    sons = []

    for sonPos in range(sonsCount):
        sonBorn = False
        while not sonBorn:
            son = []
            iSonLength = maxRange + wordLengthTolerance #initial son length
            for i in range((minRange + maxRange)/2 + min(minRange, wordLengthTolerance)):
                cut = 4 + random.randint(0,3)
                if not i >= minRange: # Inside the minRange
                    half1 = parent1[i][0:cut]
                    half2 = parent2[i][cut:]
                    gen = half1 + half2
                else: # Passing the minRange
                    if len(parent1) == maxRange and i < maxRange:
                        gen = parent1[i]
                    elif len(parent2) == maxRange and i < maxRange:
                        gen = parent2[i]
                    else: # Passing the maxRange
                        if random.random() < crossoverRate:
                            gen = parent1[random.randint(0,len(parent1)-1)]
                        else:
                            gen = parent2[random.randint(0,len(parent2)-1)]

                if random.random() <= mutationRate:
                    gen = mutate(gen)
                son.append(gen)

            # Cut the word length: Promedio entre max y min length, mas random entre min(minRange|worldLengthTolerance) negativo y lo mismo positivo
            cutWord = (minRange + maxRange)/2 + random.randint(-min(minRange, wordLengthTolerance),min(minRange, wordLengthTolerance))
            son = son[0:cutWord]

            if len(son) > 0:
                babySon = Subject(son)
                family = [c1,c2]
                family.extend(population)
                family.extend(sons)

                repeated = False
                for i in family:
                    if babySon.getAsInts() == i.getAsInts():
                        repeated = True
                        break
                if not repeated:
                    sons.append(babySon)
                    sonBorn = True
    # print("\tParents:")
    # print("\t" + c1.toString())
    # print("\t" + c2.toString())
    # print("\tSons:")
    # print("\t" + sons[0].toString())
    # print("\t" + sons[1].toString())
    return [c1, c2, sons]

def crossoverByGen(c1, c2, sonsCount = 2):
    """
    - Parameters: stronger parent, weaker parent, quantity of childs
    - The first parent is considered the more evoluted, so it has 70 percent of chance for every character of use his genes insted of the other parent
    - The crossover is made by comparing the two parents letters and length, if the sons are equal to the parents they are deleted and reprocessed
    - The large of the word is determined by: the promedy of the two parents length plus a special random int
    - The characters are determined by: The total range to iterate is determined by the largest parent, for every letter the stronger parent has 70 percent
        of chances of let its genes (his letter), the weakest has 30 percent.
        - The characters in which one parent doesn't have characters to give
    - Return: stronger parent, weakest parent , List of childs
    """
    global crossoverRate, mutationRate, tolerance, godFitness, population, wordLengthTolerance
    parent1 = c1.value
    parent2 = c2.value
    if len(parent1) >= len(parent2):
        maxRange = len(parent1)
        minRange = len(parent2)
    else:
        maxRange = len(parent2)
        minRange = len(parent1)

    sons = []

    for sonPos in range(sonsCount):
        sonBorn = False
        while not sonBorn:
            son = []
            iSonLength = maxRange + wordLengthTolerance #initial son length
            for i in range((minRange + maxRange)/2 + min(minRange, wordLengthTolerance)):
                if random.random() < crossoverRate:# Strongest parent wins the gen
                    if not i>=len(parent1):# If strongest parent enters in max Range (is the larger at last chars)
                        gen = parent1[i]
                    else:
                        if random.random() < crossoverRate:# The stronger parent has the oportunity to win again in the diferential letters
                            gen = parent1[random.randint(0,minRange-1)]# The stronger parent sets a random letter owned by it
                        else:
                            if not i>=len(parent2):
                                gen = parent2[i]
                            else:
                                gen = parent2[random.randint(0,minRange-1)]# This happens when we overpass maxRange
                else:# Weakest parent wins the gen
                    if not i>=len(parent2): # If weakest parent enters in max Range (is the larger at last chars)
                        gen = parent2[i]
                    else:
                        if random.random() < crossoverRate:# The stronger parent has the oportunity to win again in the diferential letters
                            if not i>=len(parent1):
                                gen = parent1[i]# The stronger parent sets a random letter owned by it
                            else:
                                gen = parent1[random.randint(0,minRange-1)]# This happens when we overpass maxRange
                        else:
                            gen = parent2[random.randint(0,minRange-1)]
                if random.random() <= mutationRate:
                    gen = mutate(gen)
                son.append(gen)

            # Cut the word length: Promedio entre max y min length, mas random entre min(minRange|worldLengthTolerance) negativo y lo mismo positivo
            cutWord = (minRange + maxRange)/2 + random.randint(-min(minRange, wordLengthTolerance),min(minRange, wordLengthTolerance))
            son = son[0:cutWord]

            if len(son) > 0:
                babySon = Subject(son)
                family = [c1,c2]
                family.extend(population)
                family.extend(sons)

                repeated = False
                for i in family:
                    if babySon.getAsInts() == i.getAsInts():
                        repeated = True
                        break
                if not repeated:
                    sons.append(babySon)
                    sonBorn = True
    # print("\tParents:")
    # print("\t" + c1.toString())
    # print("\t" + c2.toString())
    # print("\tSons:")
    # print("\t" + sons[0].toString())
    # print("\t" + sons[1].toString())
    return [c1, c2, sons]

def rollTheRoulete(randomly = True):
    global population
    if randomly:
        randomised = [(subject, random.random() * subject.fitScore) for subject in population]
    else:
        randomised = [(subject, subject.fitScore) for subject in population]
    sorted_ordered = sorted(randomised, key=lambda subject: subject[1])
    cleaned = [subject for subject, trash in sorted_ordered]
    result = list(reversed(cleaned))
    return result

def applyDeath(howMany = False, randomly = False):
    """
    Removes the population slowest fitscore subjects
    - If how many is false, then half the population, otherwise, the specified amount
    - If randomly is true, apply a random factor to the deletion
    """
    global population
    if howMany == False:
        howMany = len(population)/2
    if randomly:
        randomised = [(subject, random.random() * subject.fitScore) for subject in population]
    else:
        randomised = [(subject, subject.fitScore) for subject in population]
    sorted_ordered = sorted(randomised, key=lambda subject: subject[1])
    result = [subject for subject, trash in sorted_ordered]
    weakests = result[0:howMany]

    for weakSubject in weakests:
        population.pop(population.index(weakSubject))


def mutate(gen):
    global mutationLimit
    limit = mutationLimit
    genNumber = int(gen,2)
    if genNumber + limit > 255:
        limit = 255-genNumber
    if genNumber - limit < 0:
        limit = genNumber
    newGenNumber = genNumber+random.randint(-limit,limit)
    mutatedGen = format(newGenNumber,"b")[:8].zfill(8)
    # print("<<MUTATION XMEN POWER")
    # print(genNumber,newGenNumber)
    # print("\tMUTATION XMEN POWER>>")
    return mutatedGen

class Subject():

    def __init__(self,value):
        if type(value) == str:
            self.value = list(format(ord(x), 'b').zfill(8) for x in value)
        else:
            self.value = value
        self.fitScore()

    def __str__(self):
        res = ""
        for gen in self.value:
            res += chr(int(gen,2))
        return res

    def getAsInts(self):
        res = []
        for gen in self.value:
            res.append(int(gen,2))
        return res

    def toString(self):
        resStr = self.__str__()
        resInt = self.getAsInts()
        res = "| "+resStr + " | " + str(resInt) + " |"
        return res

    def wordLengthScore(self):
        global god, wordLengthMaxScore, wordLengthTolerance
        maxScore = wordLengthMaxScore
        tolerance = wordLengthTolerance

        if len(self.value)-tolerance<=len(god) or len(self.value)+tolerance>=len(god):
            res = maxScore - ((maxScore/tolerance) * abs(len(self.value)-len(god)))
        else:
            res = 0.0

        return res


    def letterEqualityScore(self):
        global god, letterEqualityMaxScore
        maxScore = letterEqualityMaxScore
        letterScore = maxScore / len(self.value)
        if len(god)<=len(self.value):
            godRange = len(god)
        else:
            godRange = len(self.value)
        res = 0
        for i in range(godRange):
            lettersDiff = abs(ord(god[i])-int(self.value[i],2))
            res += letterScore - ((letterScore/256)*lettersDiff)
        return res


    def fitScore(self):
        wordLengthScore = self.wordLengthScore()
        letterEqualityScore = self.letterEqualityScore()
        self.fitScore = wordLengthScore + letterEqualityScore
        return self.fitScore

# Main execution
adanEva()
while(True):
    rouleteOfGod()
