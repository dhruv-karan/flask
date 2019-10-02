#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 26 11:06:03 2019

@author: dhruv
"""


import pickle 

     
def load_model(filename):
    decision_tree_model_pkl = open(filename, 'rb')
    decision_tree_model = pickle.load(decision_tree_model_pkl)
    return decision_tree_model

model = load_model('weight.pkl')


col_max = [10.0, 16.0, 8.0, 33, 8.0, 5.0, 5.0, 10.0, 2.0, 10.0, 6.0]


check = [(0.0, 9.0),
 (1.0, 16.0),
 (0.0, 7.0),
 (0.0, 99.0),
 (0.0, 7.0),
 (0.0, 4.0),
 (0.0, 4.0),
 (0.0, 9.0),
 (1.0, 2.0),
 (0.0, 9.0),
 (1.0, 6.0)]







def en(d,col_max,check):
    first =1
    new = [0]*(int(sum(col_max)))
    index = 0
    i = 0
    while(index<=len(new) and i!=len(d)):
        if first == 1:
            new[int(index+int(d[i]))] = 1
            index = int(col_max[i])-1
            i +=1
            first = 0
        elif check[i][0] ==0:
            new[index+d[i]+1] = 1
            index = index + int(col_max[i])
            i+=1
        else:
            new[index+int(d[i])] = 1
            index = index + int(col_max[i])
            i+=1
    return new


def predict(d):
    a = en(d,col_max,check)
    return model.predict([a])