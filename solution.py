

def fileRead(name):
    data = []
    f = open(name, "r")
    for line in f:
        data.append(line);
    return data