#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
StudentData

生徒の情報を管理するクラス
'''

import codecs
import json
import numpy as np
import os
import pandas as pd

class StudentData:

    states = {
        0 : '志望者',
        1 : '浪人',
        2 : '仮内定',
        3 : '本内定',
        9 : '志望しない'
    }

    MAIN_DIR = os.path.abspath(os.path.dirname(__file__))
    DATA_DIR = os.path.join(MAIN_DIR,'json')
    os.makedirs(DATA_DIR,exist_ok=True)
    JSON = os.path.join(DATA_DIR,'student_data.json')

    def __init__(self):
        self.dic = 'you need to run load_dic() or create_dic() to get dic'

    # dicのデータをjsonに反映する
    def save_dic(self):
        with codecs.open(StudentData.JSON,'w',encoding='utf-8') as f:
            dump = json.dumps(self.dic,indent=2,ensure_ascii=False)
            f.write(dump)

    def load_dic(self):
        with open(StudentData.JSON,encoding='utf-8') as f:
            self.dic = json.load(f)

    def create_dic(self):
        self.dic = {}
        df = pd.read_excel('excel/input/student_data.xlsx')
        columns = ['student_num','name','destination','dest_id','is_six_course','state','final_id']
        for r in range(len(df)):
            self.dic[str(r)] = {}
            for c in columns:
                value = df.loc[r,c]
                if isinstance(value,np.integer):
                    value = int(value)
                self.dic[str(r)][c] =  value
        self.save_dic()

if __name__ == "__main__":
    s = StudentData()
    s.create_dic()
