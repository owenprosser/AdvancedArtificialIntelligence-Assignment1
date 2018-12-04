import csv, time, numpy, random

def task1A():
    probs = {
        "P(d)": float(input("Prior probability of having a disease: ")),
        "P(t|d)": float(input("Probability that the test is positive given the person has the disease: ")),
        "P(-t|-d)": float(input("Probability that the test is negative given the person does not have the disease: ")),
        "P(-d)": None,
        "P(t|-d)": None,
        "P(t)": None,
        "P(d|t)": None
    }

    probs["P(-d)"] = (1 - probs["P(d)"] )
    probs["P(t|-d)"] = (1 - probs["P(-t|-d)"])

    probs["P(t)"] = (( probs["P(t|d)"] * probs["P(d)"] ) + ( probs["P(t|-d)"] * probs["P(-d)"]))

    probs["P(d|t)"] = ((probs["P(t|d)"] * probs["P(d)"]) / probs["P(t)"])

    print("\n" + str(probs) + "\n\n")

    print("The probability of having the disease given the test was positive: " + str(probs["P(d|t)"]))

def task1B():
    variables = {
        'S':[0, 'ANX', 'PP'],
        'YF':[1, 'S'],
        'ANX':[2],
        'PP':[3],
        'G':[4],
        'AD':[5, 'G'],
        'BED':[6],
        'CA':[7, 'AD', 'F'],
        'F':[8, 'LC', 'C'],
        'A':[9],
        'C':[10, 'LC', 'A'],
        'LC':[11, 'S','G']
    }

    probs = {
        'S':[0, 0, 0, 0], #[False-False, False-True, True-False, True-True]
        'YF':[0, 0],
        'ANX':[],
        'PP':[],
        'G':[],
        'AD':[0, 0],
        'BED':[],
        'CA':[0, 0, 0, 0],
        'F':[0, 0, 0, 0],
        'A':[],
        'C':[0, 0, 0, 0],
        'LC':[0, 0, 0, 0]
    }

    for key, value in variables.items():
        #print(key, value, 'len--', len(value))
        if (len(value) == 1) :
            trueCount = 0
            totalCount = 0
            print(key, value, " No Parent")
            (trueCount, totalCount) = noParent(value[0])
            arrayLen = len(probs[key])
            print((trueCount, totalCount))
            probs[key] = ((trueCount+1)/(totalCount+2))
        elif (len(value) == 2):
            print(key, value, " 1 Parent")
            count = 0
            for i in range(2):
                probs[key][count] = oneParent(value[0], variables[value[1]], i)
                count += 1
        elif (len(value) == 3):
            print(key, value, " 2 Parents")
            parent1 = variables[value[1]]
            parent1 = parent1[0]
            parent2 = variables[value[2]]
            parent2 = parent2[0]
            print("parent 1:", parent1)
            print("parent 2:", parent2)
            print(type(parent1))
            count = 0
            for i in range(2):
                for j in range(2):
                    probs[key][count] = twoParent(value[0], parent1, parent2, i, j)
                    count += 1
        else:
            continue

    print("\n\nPrinting Probs: ")
    for key, value in probs.items():
        padding  = [' ']*(3-len(key))
        print(''.join(padding), key, " -\t", value)
    print("\n")

    priorSamplingArray = priorSampling(probs)
    smokingCountAnswer = 0
    notSmokingCountAnswer = 0
    rejectionSampling(priorSamplingArray)

def noParent(position):
    trueCount = 0
    totalCount = 0
    file = open('lucas0_train.csv', 'r')
    reader = csv.reader(file)

    for row in reader:
        if (row[position] in ['0', '1']):
            totalCount += 1
            if row[position] == '1':
                trueCount += 1

    file.close()
    return(trueCount, totalCount)

def oneParent(position, parent, x):
    print(x)
    file = open('lucas0_train.csv', 'r')
    reader = csv.reader(file)
    x_yCount = 0
    yCount = 0

    for row in reader:
        if (row[position] in ['0', '1']):
            if (row[position] == '1') and (row[parent[0]] == str(x)):
                x_yCount += 1
            if (row[parent[0]] == str(x)):
                yCount += 1

    return ((x_yCount + 1) / (yCount + 2))

    file.close()

def twoParent(position, parent1, parent2, x, y):
    print(x, y)
    file = open('lucas0_train.csv', 'r')
    reader = csv.reader(file)
    x_y_zCount = 0
    y_zCount = 0
        
    for row in reader:
        if (row[position] in ['0', '1']):
            if (row[position] == '1') and (row[parent1] == str(x)) and (row[parent2] == str(y)):
                x_y_zCount +=1
            if (row[parent1] == str(x)) and (row[parent2] == str(y)):
                y_zCount += 1
    
    returnValue = ((x_y_zCount)+1)/((y_zCount)+2)
    return(returnValue)

    file.close()

def priorSampling(probs):
    sampleSize = int(input("Enter the Number of Samples: "))
    randomArray = numpy.random.rand(sampleSize, 8)
    priorArray = numpy.zeros((sampleSize, 8))

    for i in range(sampleSize):
        for j in range(len(priorArray[0])):
            if (j == 0): #ANX
                if (randomArray[i][j] < probs['ANX']):
                    priorArray[i][j] = 1
                else:
                    priorArray[i][j] = 0
            if (j == 1): #PP
                if (randomArray[i][j] < probs['PP']):
                    priorArray[i][j] = 1
                else:
                    priorArray[i][j] = 0
            if (j == 2): #S
                if (priorArray[i][j-2] == 0) and (priorArray[i][j-1] == 0):
                    if (randomArray[i][j] < probs['S'][0]):
                        priorArray[i][j] = 1
                    else:
                        priorArray[i][j] = 0
                elif (priorArray[i][j-2] == 0) and (priorArray[i][j-1] == 1):
                    if (randomArray[i][j] < probs['S'][1]):
                        priorArray[i][j] = 1
                    else:
                        priorArray[i][j] = 0
                elif (priorArray[i][j-2] == 1) and (priorArray[i][j-1] == 0):
                    if (randomArray[i][j] < probs['S'][2]):
                        priorArray[i][j] = 1
                    else:
                        priorArray[i][j] = 0
                elif (priorArray[i][j-2] == 1) and (priorArray[i][j-1] == 1):
                    if (randomArray[i][j] < probs['S'][3]):
                        priorArray[i][j] = 1
                    else:
                        priorArray[i][j] = 0
            if (j == 3): #G
                if (randomArray[i][j] < probs['G']):
                    priorArray[i][j] = 1
                else:
                    priorArray[i][j] = 0
            if (j == 4): #LC
                if (priorArray[i][j-2] == 0) and (priorArray[i][j-1] == 0):
                    if (randomArray[i][j] < probs['LC'][0]):
                        priorArray[i][j] = 1
                    else:
                        priorArray[i][j] = 0
                elif (priorArray[i][j-2] == 0) and (priorArray[i][j-1] == 1):
                    if (randomArray[i][j] < probs['LC'][1]):
                        priorArray[i][j] = 1
                    else:
                        priorArray[i][j] = 0
                elif (priorArray[i][j-2] == 1) and (priorArray[i][j-1] == 0):
                    if (randomArray[i][j] < probs['LC'][2]):
                        priorArray[i][j] = 1
                    else:
                        priorArray[i][j] = 0
                if (priorArray[i][j-2] == 1) and (priorArray[i][j-1] == 1):
                    if (randomArray[i][j] < probs['LC'][3]):
                        priorArray[i][j] = 1
                    else:
                        priorArray[i][j] = 0
            if (j == 5): #A
                if (randomArray[i][j] < probs['A']):
                    priorArray[i][j] = 1
                else:
                    priorArray[i][j] = 0
            if (j == 6): #C
                if (priorArray[i][j-2] == 0) and (priorArray[i][j-1] == 0):
                    if (randomArray[i][j] < probs['C'][0]):
                        priorArray[i][j] = 1
                    else:
                        priorArray[i][j] = 0
                elif (priorArray[i][j-2] == 0) and (priorArray[i][j-1] == 1):
                    if (randomArray[i][j] < probs['C'][1]):
                        priorArray[i][j] = 1
                    else:
                        priorArray[i][j] = 0
                elif (priorArray[i][j-2] == 1) and (priorArray[i][j-1] == 0):
                    if (randomArray[i][j] < probs['C'][2]):
                        priorArray[i][j] = 1
                    else:
                        priorArray[i][j] = 0
                if (priorArray[i][j-2] == 1) and (priorArray[i][j-1] == 1):
                    if (randomArray[i][j] < probs['C'][3]):
                        priorArray[i][j] = 1
                    else:
                        priorArray[i][j] = 0
            if (j == 7): #F
                if (priorArray[i][j-2] == 0) and (priorArray[i][j-1] == 0):
                    if (randomArray[i][j] < probs['F'][0]):
                        priorArray[i][j] = 1
                    else:
                        priorArray[i][j] = 0
                elif (priorArray[i][j-2] == 0) and (priorArray[i][j-1] == 1):
                    if (randomArray[i][j] < probs['F'][1]):
                        priorArray[i][j] = 1
                    else:
                        priorArray[i][j] = 0
                elif (priorArray[i][j-2] == 1) and (priorArray[i][j-1] == 0):
                    if (randomArray[i][j] < probs['F'][2]):
                        priorArray[i][j] = 1
                    else:
                        priorArray[i][j] = 0
                if (priorArray[i][j-2] == 1) and (priorArray[i][j-1] == 1):
                    if (randomArray[i][j] < probs['F'][3]):
                        priorArray[i][j] = 1
                    else:
                        priorArray[i][j] = 0

    #print(priorArray)
    return(priorArray)

def rejectionSampling(prior):
    smokingCount = 0
    notSmokingCount = 0
    for i in range(len(prior)):
        if (prior[i][2] == 1) and (prior[i][6] == 1) and (prior[i][7] == 1):
            smokingCount += 1
        elif (prior[i][2] == 0) and (prior[i][6] == 1) and (prior[i][7] == 1):
            notSmokingCount += 1

    smokingCountAnswer = smokingCount/len(prior)
    notSmokingCountAnswer = notSmokingCount/len(prior)

    normalise(smokingCountAnswer, notSmokingCountAnswer)

def normalise(smokingCountAnswer, notSmokingCountAnswer):
    print("normalise")
    print(smokingCountAnswer, notSmokingCountAnswer)

    alpha = 1/(smokingCountAnswer + notSmokingCountAnswer)
    normSmokingCountAnswer = smokingCountAnswer * alpha
    normNotSmokingCountAnswer = notSmokingCountAnswer * alpha
    print("Normalised Values:")
    print(normSmokingCountAnswer, normNotSmokingCountAnswer)
    print("Probability Smoking given Coughing and Fatigue (P|S,F): ", normSmokingCountAnswer)

def task2():
    sequence = []
    
    while (len(sequence) < 1):
        userInput = input("Enter Sequence of Symbols: ")
        for index, item in enumerate(userInput):
            if item not in ['c', 'w', 'h']:
                continue
            else:
                sequence.append(userInput[index])

    matrices = {
        'c': [[0.3, 0],
              [0, 0.45]],

        'h':  [[0.35, 0],
               [0, 0.1]],

        'w': [[0.35, 0],
              [0, 0.45]],

        'Transition': [[0.6, 0.4],
                   [0.4, 0.6]],

        'initial':[0.5, 0.5]
    }

    for item in sequence:
        matrices['initial'] = smallProduct(dotProduct(matrices[item], matrices['Transition']), matrices['initial'])
        print(matrices['initial'])

    print("\nProbability of observing the sequence: ", sequence, "is:\n", sum(matrices['initial']))
    #print(sum(matrices['initial']))

def dotProduct(matrixA, matrixB):
    if (len(matrixA) == len(matrixB)) and (len(matrixA[0]) == len(matrixB[0])):
        tempArray = [[None]*len(matrixA),[None]*len(matrixA[0])]
        #print("\nArrays of same dimensions")

        tempArray[0][0] = ((matrixA[0][0] * matrixB[0][0]) + (matrixA[0][1] * matrixB[1][0]))
        tempArray[0][1] = ((matrixA[0][0] * matrixB[0][1]) + (matrixA[0][1] * matrixB[1][1]))
        tempArray[1][0] = ((matrixA[1][0] * matrixB[0][0]) + (matrixA[1][1] * matrixB[1][0]))
        tempArray[1][1] = ((matrixA[1][0] * matrixB[0][1]) + (matrixA[1][1] * matrixB[1][1]))

        return(tempArray)
    else:
        print("Arrays of different dimensions")
        return(1)

def smallProduct(matrix, smallMatrix):
    returnMatrix = [None, None]
    count = 0
    smallCount = 0

    returnMatrix[0] = (matrix[0][0]*smallMatrix[0]) + (matrix[0][1]*smallMatrix[1])
    returnMatrix[1] = (matrix[1][0]*smallMatrix[0]) + (matrix[1][1]*smallMatrix[1])

    return(returnMatrix)

def menu():
    while (True):
        print("\n\nOwen Prosser - PRO14514822 - Advanced Artificial Inteligence - CMP9132M")
        userInput = None
        print("1: Task 1a")
        print("2: Task 1b")
        print("3: Task 2")
        userInput = str(input())
        if userInput[0] in ['1', '2', '3']:
            if userInput[0] == "1":
                task1A()
            elif userInput[0] == '2':
                task1B()
            elif userInput[0] == '3':
                task2()
        else:
            continue

if __name__ == "__main__":
    menu()