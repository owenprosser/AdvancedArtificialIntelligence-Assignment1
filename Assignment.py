import csv, time, numpy

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
        'S':[],
        'YF':[],
        'ANX':[],
        'PP':[],
        'G':[],
        'AD':[],
        'BED':[],
        'CA':[],
        'F':[],
        'A':[],
        'C':[],
        'LC':[]
    }

    for key, value in variables.items():
        #print(key, value, 'len--', len(value))
        if (len(value) == 1):
            trueCount = 0
            totalCount = 0
            print(key, value, " 1 Parent")
            (trueCount, totalCount) = oneParent(value[0])
            print((trueCount, totalCount))
            probs[key] = ((trueCount+1)/(totalCount+2))
        elif (len(value) == 2):
            trueCount = 0
            totalCount = 0
            yCount = 0
            print(key, value, " 2 Parents")
            (trueCount, yCount, totalCount) = twoParent(value[0], variables[value[1]])
            print((trueCount, yCount, totalCount))
            probs[key] = ((trueCount+1)/(yCount+2))
        elif (len(value) == 3):
            trueCount = 0
            totalCount = 0
            yCount = 0
            totalCount = 0
            print(key, value, " 3 Parents")
            parent1 = variables[value[1]]
            parent1 = parent1[0]
            parent2 = variables[value[2]]
            parent2 = parent2[0]
            print("parent 1:", parent1)
            print("parent 2:", parent2)
            print(type(parent1))
            (trueCount, yCount, totalCount) = twoParent(value[0], variables[value[1]])
            print((trueCount, totalCount))
            probs[key] = ((trueCount+1)/(yCount+2))
        else:
            continue

    print("\n\nPrinting Probs: ")
    for key, value in probs.items():
        padding  = [' ']*(3-len(key))
        print(''.join(padding), key, " -\t", round(value, 4))

def oneParent(position):
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

def twoParent(position, parent):
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

def threeParent(position, parent1, parent2):
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

def task2():
    sequence = []
    
    while (len(sequence) < 1):
        userInput = input("Enter Sequence of Symbols: ")
        for index, item in enumerate(userInput):
            if item not in ['c', 'w', 'h']:
                continue
            else:
                sequence.append(userInput[index])

    print(sequence)

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

    for key, value in matrices.items():
        print(key, value)

    for item in sequence:
        matrices['initial'] = smallProduct(dotProduct(matrices[item], matrices['Transition']), matrices['initial'])
        print(matrices['initial'])
    
    print(matrices['initial'])
    print(sum(matrices['initial']))

def dotProduct(matrixA, matrixB):
    if (len(matrixA) == len(matrixB)) and (len(matrixA[0]) == len(matrixB[0])):
        tempArray = [[0]*len(matrixA)]*len(matrixA[0])
        print("\nArrays of same dimensions")

        tempArray = numpy.dot(matrixA, matrixB)

        print(tempArray)
        return(tempArray)
    else:
        print("Arrays of different dimensions")
        return(1)

def smallProduct(matrix, smallMatrix):
    returnMatrix = [None, None]
    count = 0

    for item in matrix:
        returnMatrix[count] = sum(item)*smallMatrix[count]
        count += 1

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