import csv, time

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
        'S':[0, 'A', 'PP'],
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
        'YF':[],
        'ANX':[],
        'PP':[],
        'G':[],
        'AD':[],
        'BED':[],
        'CA':[0, 0, 0, 0],
        'F':[0, 0, 0, 0],
        'A':[],
        'C':[0, 0, 0, 0],
        'LC':[0, 0, 0, 0]
    }

    for key, value in variables.items():
        #print(key, value, 'len--', len(value))
        if (len(value) == 1) and (False):
            trueCount = 0
            totalCount = 0
            print(key, value, " No Parent")
            (trueCount, totalCount) = noParent(value[0])
            arrayLen = len(probs[key])
            print((trueCount, totalCount))
            probs[key] = ((trueCount+1)/(totalCount+2))
        elif (len(value) == 2) and (False):
            trueCount = 0
            totalCount = 0
            yCount = 0
            print(key, value, " 1 Parent")
            (trueCount, yCount, totalCount) = oneParent(value[0], variables[value[1]])
            print((trueCount, yCount, totalCount))
            probs[key] = ((trueCount+1)/(yCount+2))
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
                    probs[key][count] = twoParentTest(value[0], parent1, parent2, i, j)
                    count += 1
        else:
            continue

    print("\n\nPrinting Probs: ")
    for key, value in probs.items():
        padding  = [' ']*(3-len(key))
        print(''.join(padding), key, " -\t", value)

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

def oneParent(position, parent):
    print("Parent is:", str(parent[0]))
    trueCount = 0
    yCount = 0
    totalCount = 0
    file = open('lucas0_train.csv', 'r')
    reader = csv.reader(file)

    for row in reader:
        if (row[position] in ['0', '1']) and (row[parent[0]] in ['0', '1']):
            totalCount += 1
            if (row[parent[0]] == '1'):
                yCount += 1
                if (row[position] == '1'):
                    trueCount += 1

    file.close()
    return(trueCount, yCount, totalCount)

def twoParent(position, parent1, parent2):
    trueCount = 0
    yCount  = 0
    zCount = 0
    totalCount = 0
    file = open('lucas0_train.csv', 'r')
    reader = csv.reader(file)

    for row in reader:
        if (row[position] in ['0', '1']) and (row[parent1] in ['0', '1']) and (row[parent1] in ['0', '1']):
            totalCount += 1
            if row[position] == '1':
                if row[parent1] == '1':
                    if row[parent2] == '1':
                        trueCount += 1
            if row[parent1] == '1':
                if row[parent2] == '1':
                    yCount += 1

    file.close()
    return(trueCount, yCount, totalCount)

def twoParentTest(position, parent1, parent2, x, y):
    print(x, y)
    file = open('lucas0_train.csv', 'r')
    reader = csv.reader(file)
    xCount = 0
    yCount = 0
    zCount = 0
        
    for row in reader:
        if (row[position] in ['0', '1']):
            if (row[position] == '1'):
                xCount += 1
            if (row[parent1] == str(x)):
                yCount += 1
            if (row[parent2] == str(y)):
                zCount += 1
    
    print(xCount, yCount, zCount)
    returnValue = ((xCount+yCount+zCount)+1)/((yCount+zCount)+2)
    return(returnValue)

    file.close()

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