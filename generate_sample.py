#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
くじ引きのサンプル情報を作る
'''

import numpy as np
import os
import pandas as pd

from Students import Student


MAIN_DIR = os.path.abspath(os.path.dirname(__file__))
EXCEL = os.path.join(MAIN_DIR, 'excel', 'lab_data2.xlsx')
EXCEL2 = os.path.join(MAIN_DIR, 'excel', 'after_first.xlsx')
EXCEL3 = os.path.join(MAIN_DIR, 'excel', 'haizoku2.xlsx')
LAB_NUM = 22

def set_sample(num):
    candidates = []
    for i in range(1,num+1):
        s = Student()
        s.id = i
        s.name = 'Student' + str(i)
        if num < 9:
            s.is_six_cource = True
        s.destination_id = np.random.randint(LAB_NUM)
        candidates.append(s)
    return candidates
candidates = set_sample(89)
print(candidates[0])

pd.read_excel(EXCEL)

def set_sample2(num):
    candidates = []
    data = pd.read_excel(EXCEL3)


def first_lottery(array):
    df = pd.read_excel(EXCEL)
    result_array  = []
    box2d = []
    for _ in range(LAB_NUM):
        box2d.append([])
    np.random.shuffle(array)
    for student in array:
        four_year = df.loc[student.destination_id].four_year
        six_year  = df.loc[student.destination_id].six_year
        both      = df.loc[student.destination_id].both
        dest_id   = student.destination_id
        if student.is_six_cource:
            if len(box2d[dest_id]) < six_year + both:
                student.state = Student.states[2]
                student.lab_id = dest_id
                box2d[dest_id].append(student.id)
            else:
                student.state = Student.states[1]
        else:
            if len(box2d[dest_id]) < four_year + both:
                student.state = Student.states[2]
                student.lab_id = dest_id
                box2d[dest_id].append(student.id)
            else:
                student.state = Student.states[1]
        result_array.append(student)
    for i,line in enumerate(box2d):
        for j,id in enumerate(line):
            row = 's' + str(j+1)
            df.loc[i,row] = id
    df.to_excel(EXCEL2)
    print([s.id for s in result_array if s.state == Student.states[1]])
    return result_array

def main():
    candidates = set_sample(89)
    result = first_lottery(candidates)

if __name__ == '__main__':
    main()
