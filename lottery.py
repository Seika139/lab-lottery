#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
全体のくじの流れ
'''

# delete below
import codecs
import json

import numpy as np
import os
import pandas as pd

from Students import Student

# MAIN_DIR = os.path.abspath(os.path.dirname(__file__))
# delete below
MAIN_DIR = '/Users/suzukikenichi/pro-main/lab-lottery'
EXCEL = os.path.join(MAIN_DIR, 'excel', 'lab_data.xlsx')

df = pd.read_excel(EXCEL)

lab_num = 24

with codecs.open('test.json','w',encoding='utf-8') as f:
        dump = json.dumps(dic,indent=2,ensure_ascii=False)
        f.write(dump)

def set_sample(num):
    candidates = []
    for i in range(num):
        s = Student()
        s.destination = np.random.randint(0,lab_num)
        s.name = 'student'+str(i)
        candidates.append(s)
    return candidates

def first_lottery(candidates):
    box2d = []
    for _ in range(lab_num):
        box2d.append([])
    for student in candidates:
        box2d[student.destination].append(student.name)
    return box2d

npr = first_lottery(set_sample(80))

df['candidates'] = npr
df
