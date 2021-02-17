import os

path = "/Users/jakob/OneDrive/KBE/PythonKBE/TableAssignment/DFA"
dirname = os.path.dirname(__file__)
pathToDFA = dirname + "/DFA"


def DFA_RW(topL, topW, topH, legL, legW, legH):
    # Read the content of the template file
    f = open(pathToDFA + "/Templates/TableTemplate.dfa", "r")
    data = f.read()

    data = data.replace("<topL>", str(topL))
    data = data.replace("<topW>", str(topW))
    data = data.replace("<topH>", str(topH))
    data = data.replace("<legL>", str(legL))
    data = data.replace("<legW>", str(legW))
    data = data.replace("<legH>", str(legH))

    f = open(pathToDFA + "/myTable.dfa", "w+")
    f.write(data)
    f.close()
