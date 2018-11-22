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

    print( str(probs) + "\n\n")

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
            print(key, value, " 2 Parents")
            (trueCount, totalCount) = twoParent(value[0], variables[value[1]])
            print((trueCount, totalCount))
            probs[key] = ((trueCount+1)/(totalCount+2))
        else:
            continue

    print("\n\nPrinting Probs: ")
    for key, value in probs.items():
        print(key, value)

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
    totalCount = 0
    file = open('lucas0_train.csv', 'r')
    reader = csv.reader(file)

    for row in reader:
        if (row[position] in ['0', '1']) and (row[parent[0]] in ['0', '1']):
            totalCount += 1
            if row[position] == '1':
                trueCount += 1

    file.close()
    return(trueCount, totalCount)

def task2():
    userInput = input("Enter Sequence of Symbols: ")
    sequence = []

    for index, item in enumerate(userInput):
        if item not in ['c', 'w', 'h']:
            continue
        else:
            sequence.append(userInput[index])

    print(sequence)

if __name__ == "__main__":
    #task1A()
    task1B()
    #task2()