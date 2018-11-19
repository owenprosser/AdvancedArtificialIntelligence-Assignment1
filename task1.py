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
    probs["P(t|-d)"] = (1 - probs["P(t|d)"])
    
    probs["P(t)"] = ( probs["P(t|d)"] * probs["P(d)"] ) + ( probs["P(t|-d)"] * probs["P(-d)"])

    probs["P(d|t)"] = (probs["P(t|d)"] * probs["P(d)"]) / probs["P(t)"]

    print(probs)

if __name__ == "__main__":
    task1A()