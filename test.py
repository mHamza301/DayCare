#initialize all files of all rooms to zero
# import the necessary packages
from imutils import paths
import pickle
import sys

if __name__ == '__main__' :
    # construct the argument parser and parse the arguments
    encodings = 'F://FYP 2019-2020//Facial Recognition Python//encodingsTset.pickle'

    # grab the paths to the encodings that contains names
    data = pickle.loads(open(encodings, "rb").read())
    NamesOnce = {}

    for i in data["names"]:
        name = i
        NamesOnce[name] = 0

    #print(NamesOnce)

    #initialize the Room1 and Room2 Files
    print("[INFO] Creating files...")
    f1 = open("F://FYP 2019-2020//Facial Recognition Python//output//Room1.txt", "w+")
    for xname in NamesOnce:
        f1.write(xname + "\t\t" + str(NamesOnce[xname]) + "\n")
    f1.close()
    f2 = open("F://FYP 2019-2020//Facial Recognition Python//output//Room2.txt", "w+")
    for xname in NamesOnce:
        f2.write(xname + "\t\t" + str(NamesOnce[xname]) + "\n")
    f2.close()
        