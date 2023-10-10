import dearpygui.dearpygui as dpg
import json
import datetime
import os
import shutil

def LoadHighscore():
    names = []
    scores = []

    file = open("highscore.cfg", 'r')
    data = json.load(file)
    names = data['names']
    scores = data['scores']
    
    return names,scores

def UpdateHighScore(name, score):
    newScores = [None] * 10
    newNames = [None] * 10
    names = []
    scores = []
    scoreplaced = False
    indexZeroIsNew = False

    names, scores = LoadHighscore()


    indexForNewScore = 0 
    for i , evt in enumerate(scores):
        if i == 0 and scoreplaced == False and score > scores[i] and indexZeroIsNew == False:
            newNames[i] = name
            newScores[i] = score
            scoreplaced = True
            indexZeroIsNew = True
        elif i > 0 and scoreplaced == True and indexZeroIsNew == True:
            newScores[i] = scores[i-1]
            newNames[i] = names[i-1]
        
        if i > 0 and scoreplaced == False and score > scores[i] and indexZeroIsNew == False:
            newNames[i] = name
            newScores[i] = score
            indexForNewScore = i
            scoreplaced = True
            for j in range(0, indexForNewScore):
                newNames[j] = names[j]
                newScores[j] = scores[j]
        elif i > indexForNewScore and scoreplaced == True and indexZeroIsNew == False: 
            newScores[i] = scores[i-1]
            newNames[i] = names[i-1]

    SaveHighScore(newNames, newScores)

def SaveHighScore(names, scores):

    config = {
            "names": names,
            "scores": scores
        }
    nameOfFile =  str('highscore.cfg')
    with open(nameOfFile, 'w') as c:
        c.write(json.dumps(config, indent=4))