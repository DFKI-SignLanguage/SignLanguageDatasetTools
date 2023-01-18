# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 00:33:46 2022

@author: Fabian Deckert
"""

def readcsv(name, sep):
    d = open(name)
    ht = []
    cat = d.readline().split(sep)
    for line in d:
        a = line.split(sep)
        ht.append(a)
    return cat, ht

def createcsv(name, sep, cat, ht):
    d = open(name, "x")
    for t in range(0,len(cat)):
        d.write(cat[t])
        if t == len(cat)-1:
            continue
        d.write(sep)
    d.write("\n")
    for el in range(0,len(ht)):
        d.write(ht[el])
        if (el+1) % len(cat) == 0:
            d.write("\n")
        else: 
            d.write(sep)
    d.close()
    
def appendcsv(name, sep, cat, ht):
    d = open(name, "a")
    d.write("\n")
    for el in range(0,len(ht)):
        d.write(ht[el])
        if (el+1) % len(cat) == 0:
            d.write("\n")
        else: 
            d.write(sep)
    d.close()
    
def writecsv(name, sep, cat, ht):
    try:
        createcsv(name, sep, cat, ht)
    except:
        appendcsv(name, sep, cat, ht)