#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
全体くじのプログラム
'''

import numpy as np
import os
import pandas as pd

from Students import Student

MAIN_DIR = os.path.abspath(os.path.dirname(__file__))
EXCEL = os.path.join(MAIN_DIR, 'excel', 'for_second_lottery.xlsx')
EXCEL = os.path.join(MAIN_DIR, 'excel', 'after_first.xlsx')
df = pd.read_excel(EXCEL)

def get_candidates_from_xlsx():
    dic = {}
    candidates = []
    columns = ['s'+str(i) for i in range(1,7)]
    for r in range(len(df)):
        for c in columns:
            id = df.loc[r,c]
            if id==id:
                s = Student()
                s.id = int(id)
                s.state = Student.states[2]
                s.lab_id = df.loc[r,'id']
                if s.lab_id in dic:
                    dic[s.lab_id]['students'].append(s.id)
                else:
                    dic[s.lab_id] = {
                        'students' : [s.id],
                        'min' : df.loc[r,'min']
                    }
                candidates.append(s)
    return candidates, dic

def find_lack_lab(dic):
    lack_labs = []
    for key in dic:
        if dic[key]['min'] > len(dic[key]['students']):
            lack_labs.append([key,dic[key]['min']-len(dic[key]['students'])])
    return lack_labs


def second_lottery():
    # フォームの情報を整えた辞書を作る
    dic = {}
    with open('form_raw.txt', 'r') as f:
        form = f.readlines()
    for l in form:
        lab, id = l.split('\t')
        id = int(id.split('\n')[0])
        if lab in dic:
            dic[lab].append(id)
        else:
            dic[lab] = [id]

    print(dic)

    max_lab = 0
    min_lab = 100
    for key in dic:
        min_lab = min(min_lab,len(dic[key]))
        max_lab = max(max_lab,len(dic[key]))
    print(max_lab,min_lab)

    if max_lab / min_lab > 2:
        all_lottery()
    else:
        # separate_lottery()
        pass

def all_lottery(cand,lack_labs):
    l = [i for i in range(1,90)]
    np.random.shuffle(l)
    print(l)
    """
    num_move = 0
    for i in lack_labs:
        num_move += i[1]
    print(num_move)
    np.random.shuffle(cand)
    for students in cand:
        pass
    """

def lottery(cand):
    np.random.shuffle(cand)


def main():
    cand, dic = get_candidates_from_xlsx()
    lack_labs = find_lack_lab(dic)
    second_lottery()
    print(len(cand))
    print(all_lottery(0,0))


if __name__ == "__main__":
    main()
