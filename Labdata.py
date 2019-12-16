#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
LabData

研究室の情報を管理するクラス
'''

import codecs
import json
import numpy as np
import os
import pandas as pd

class LabData:

    MAIN_DIR = os.path.abspath(os.path.dirname(__file__))
    DATA_DIR = os.path.join(MAIN_DIR,'json')
    os.makedirs(DATA_DIR,exist_ok=True)
    JSON = os.path.join(DATA_DIR,'lab_data.json')

    def __init__(self):
        self.dic = 'you need to run load_dic() or create_dic() to get dic'

    # dicのデータをjsonに反映する
    def save_dic(self):
        with codecs.open(LabData.JSON,'w',encoding='utf-8') as f:
            dump = json.dumps(self.dic,indent=2,ensure_ascii=False)
            f.write(dump)

    def load_dic(self):
        with open(LabData.JSON,encoding='utf-8') as f:
            self.dic = json.load(f)

    def create_dic(self):
        self.dic = {}
        df = pd.read_excel('excel/input/lab_data.xlsx')
        columns = ['name', 'common_name', 'min', 'four_year', 'six_year', 'both']
        for r in range(len(df)):
            self.dic[str(r)] = {}
            for c in columns:
                value = df.loc[r,c]
                if isinstance(value,np.integer):
                    value = int(value)
                self.dic[str(r)][c] =  value
            self.dic[str(r)]['enrollee'] = []
        self.save_dic()

    def int_to_str(self,n):
        if type(n) == int:
            return str(n)
        else:
            return n

    def add_student(self,lab,id):
        lab = self.int_to_str(lab)
        id = self.int_to_str(id)
        self.dic[lab]['enrollee'].append(id)

    def delete_student(self,id):
        id = self.int_to_str(id)
        keys = [d[0] for d in self.dic.items() if id in d[1]['enrollee']]
        for key in keys:
            self.dic[key]['enrollee'] = [i for i in self.dic[key]['enrollee'] if i != id]

    def move_student(self,new_lab,id):
        self.delete_student(id)
        self.add_student(new_lab,id)

    def get_lacking_labs(self):
        """
        不足枠の研究室を取得する
        return -> 要素が [研究室のid,不足人数] からなる二重配列
        """
        lacking_labs = []
        for key in self.dic:
            n = self.dic[key]['min'] - len(self.dic[key]['enrollee'])
            if n > 0:
                lacking_labs.append([key,n])
        return lacking_labs

    def get_open_labs(self,is_six_course):
        """
        空き枠の研究室を取得する
        return -> 空き枠のある研究室のidからなる配列
        """
        open_labs = []
        for key in self.dic:
            if is_six_course == 1:
                n = self.dic[key]['six_year'] + self.dic[key]['both']
                if len(self.dic[key]['enrollee']) < n:
                    open_labs.append(key)
            else:
                n = self.dic[key]['four_year'] + self.dic[key]['both']
                if len(self.dic[key]['enrollee']) < n:
                    open_labs.append(key)
        return open_labs

# delete below
if __name__ == "__main__":
    s = LabData()
    s.create_dic()
    # s.load_dic()
    # # s.add_student(0,2)
    for i in range(10):
        s.move_student(i,i+1)
    s.save_dic()
