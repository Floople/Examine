import os
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import numpy as np
import sys
import shutil
from scipy.stats import entropy

def makeGraph(words1, name, graphTitle):
    if not bool(words1):
        plt.barh(range(len(words1)), words1.values())
        plt.xlabel('frequency', fontsize=18)
        plt.ylabel('keywords', fontsize=18)
        plt.title(graphTitle)
    else:
        temp3 = sorted(words1.items(), key = lambda kv:(kv[1], kv[0]))
        wordList = zip(*temp3)[0]
        #print(wordList)
        freq = zip(*temp3)[1]
        #print(freq)
        y_pos = np.arange(len(wordList))
        plt.barh(y_pos, freq)
        plt.title(graphTitle)
        plt.yticks(y_pos,wordList)
        plt.xlabel('frequency', fontsize=18)
        plt.ylabel('keywords', fontsize=18)
    plt.savefig(name)


def makeScatterPlot(listWords1):
    for dic in listWords1:
        for key in wordsMean:
            if key.lower() not in dic:
                dic[key.lower()] = float(0)
    temp5 = sorted(wordsMean.items(), key = lambda kv: (kv[0], kv[1]))
    #print(temp5)
    meanFreq = zip(*temp5)[1]
    p = np.asarray(meanFreq)
    p /= p.sum()
    for dic in listWords1:
        #if not bool(dic):
            #continue
        temp4 = sorted(dic.items(), key = lambda kv:(kv[0], kv[1]))
        #print(temp4)
        thisFreq = zip(*temp4)[1]
        q = np.asarray(thisFreq)
        #print(q)
        m = 0.5 * (p + q)
        #print(m)
        np.seterr(divide='ignore', invalid='ignore')
        jsdNum = 0.5 * (entropy(p,m) + entropy(q,m))
        jsd.append(jsdNum)
    z = 0
    while z < len(jsd):
        if np.isnan(jsd[z]):
            jsd[z] = 1
        z += 1

    #make scatter plt
    plt.scatter(jsd, fileList)
    plt.title("summary_JSD")
    plt.xlabel('JSD value', fontsize=18)
    plt.ylabel('textfiles', fontsize=18)
    plt.savefig(nameScatter)


base = os.getcwd()
directoryComplete = []
temp = sys.argv[1:]
for i in temp:
    directoryComplete.append(os.path.join(base,i))
path = base
jsd = []
words = {}
listWords = []
fileList = []
wordsMean = {}
counter = 0
textCounter = 0
for root, dirs, files in os.walk(path):
    for file in files:
        if file.endswith(".txt") and root in directoryComplete and file not in fileList:
            textCounter += 1
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
            fileList.append(file)
            listWords.append(words)
            makeGraph(words1 = words, name = name, graphTitle = graphTitle)
            words = {}
            plt.clf()
            shutil.move(os.path.join(base,name), os.path.join(root,name))
        if file is files[-1] and bool(listWords):
            #summary dist
            for dic in listWords:
                for key in dic:
                    if key.lower() in wordsMean:
                        wordsMean[key.lower()] += float(1)
                    else:
                        wordsMean[key.lower()] = float(1)
            for m in wordsMean:
                wordsMean[m] = float(wordsMean[m]) / textCounter
            textCounter = 0
            nameMean = "summary_meanDist.png"
            titleMean = "summary_meanDist"
            makeGraph(words1 = wordsMean, name = nameMean, graphTitle = titleMean)
            shutil.move(os.path.join(base,nameMean), os.path.join(root,nameMean))
            plt.clf()
            #scatter plot
            nameScatter = "summary_JSDplot.png"
            makeScatterPlot(listWords1 = listWords)
            shutil.move(os.path.join(base,nameScatter), os.path.join(root,nameScatter))
            fileList = []
            jsd = []
            listWords = []
            plt.clf()
            wordsMean = {}