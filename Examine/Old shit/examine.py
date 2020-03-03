import os
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import numpy as np
import sys
import shutil
def makeGraph(words1, name, graphTitle):
    temp3 = (sorted(words.items(), key = lambda kv:(kv[1], kv[0])))
    wordList = zip(*temp3)[0]
    freq = zip(*temp3)[1]
    y_pos = np.arange(len(wordList))
    plt.barh(y_pos, freq)
    counter = 0
    plt.title(graphTitle)
    plt.yticks(y_pos,wordList)
    plt.xlabel('frequency', fontsize=18)
    plt.ylabel('keywords', fontsize=18)
    plt.savefig(name)
base = os.getcwd()
directoryComplete = []
temp = sys.argv[1:]
for i in temp:
    directoryComplete.append(os.path.join(base,i))
path = base
words = {}
counter = 0
for root, dirs, files in os.walk(path):
    for file in files:
        if file.endswith(".txt") and root in directoryComplete:
            words.clear()
            plt.clf()
            temp2 = file.split('.')
            name = temp2[0]  + "_hist.png"
            graphTitle = temp2[0] + "_hist"
            with open(os.path.join(root,file), "r") as textFile:
                for line in textFile:
                    for word in line.strip().split(' '):
                        counter += 1
                        if word.isalpha() and word != '':
                            if word.lower() in words:
                                words[word.lower()] += float(1)
                            else:
                                words[word.lower()] = float(1)
            for i in words:
                words[i] = float(words[i]) / counter
            counter = 0
            makeGraph(words1 = words, name = name, graphTitle = graphTitle)
            shutil.move(os.path.join(base,name), os.path.join(root,name))
