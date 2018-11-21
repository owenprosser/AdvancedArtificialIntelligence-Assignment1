import csv

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
    file = open('lucas0_train.csv', 'rb')
    reader = csv.reader(file)
    for row in reader:
        print(row)
    file.close()

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
    #task1B()
    task2()