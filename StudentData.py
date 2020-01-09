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
        '0' : '未配属',
        '1' : '浪人',
        '2' : '仮内定',
        '3' : '本内定',
        '7' : '無断欠席',
        '8' : '志望しない',
        '9' : '在籍していない',
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
        # 実験用
        df = pd.read_excel('excel/input/student_data.xlsx')
        columns = ['student_num','name','destination','dest_id','is_six_course','state','final_id']
        for r in range(len(df)):
            self.dic[str(r)] = {}
            for c in columns:
                value = df.loc[r,c]
                if isinstance(value,np.integer):
                    value = str(int(value))
                self.dic[str(r)][c] =  value
        self.save_dic()

    def get_vagabonds(self):
        vagabonds = [k for k,v in self.dic.items() if v['state']=='1']
        return vagabonds

    def get_provisionals(self):
        provisionals = [k for k,v in self.dic.items() if v['state']=='2']
        return provisionals

    def finalize(self):
        for key in self.dic:
            if self.dic[key]['state'] == '2':
                self.dic[key]['state'] = '3'
        self.save_dic()
