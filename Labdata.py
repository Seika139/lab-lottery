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
            self.dic[str(r)]['enrollee'] =  [[],[],[]]
        self.save_dic()

    def get_id_from_name(self, name):
        reverse_dic = {}
        for key in self.dic:
            reverse_dic[self.dic[key]['name']] = key
        if name in reverse_dic:
            return reverse_dic[name]
        else:
            return None

    def int_to_str(self,n):
        if type(n) == int:
            return str(n)
        else:
            return n

    def get_capacities(self,lab):
        """
        four_year, six_year, both にそれぞれ空きがあるかをbool値で示す
        return -> [bool,bool,bool]
        """
        capacities = []
        for i in range(3):
            capacities.append(len(self.dic[lab]['enrollee'][i]) < self.dic[lab][['four_year', 'six_year', 'both'][i]])
        return capacities

    def add_student(self,lab,id,is_six):
        """
        idの生徒をlabに配属する
        return -> True なら配属成功
        """
        lab = self.int_to_str(lab)
        id = self.int_to_str(id)
        capacities = self.get_capacities(lab)
        if is_six and capacities[1]:
            self.dic[lab]['enrollee'][1].append(id)
            return True
        elif not is_six and capacities[0]:
            self.dic[lab]['enrollee'][0].append(id)
            return True
        elif capacities[2]:
            self.dic[lab]['enrollee'][2].append(id)
            return True
        else:
            return False

    def delete_student(self,id):
        """
        idの生徒をdicから削除する
        """
        id = self.int_to_str(id)
        keys = [d[0] for d in self.dic.items() if search_elem(id,d[1]['enrollee'])]
        for key in keys:
            self.dic[key]['enrollee'] = [[i for i in l if i != id] for l in self.dic[key]['enrollee']]

    def move_student(self,new_lab,id,is_six):
        """
        idの生徒をlabに移動
        return -> True なら移動成功
        """
        if self.able_to_receive(new_lab,is_six):
            self.delete_student(id)
            tf = self.add_student(new_lab,id,is_six)
            return tf
        else:
            return False

    def get_lacking_labs(self):
        """
        不足枠の研究室を取得する
        return -> 要素が [研究室のid,不足人数] からなる二重配列
        """
        lacking_labs = []
        for key in self.dic:
            n = self.get_lacking_num_by_id(key)
            if n > 0:
                lacking_labs.append([key,n])
        return lacking_labs

    def get_lacking_num_by_id(self,lab):
        """
        labの研究室の不足人数を返す
        不足していない場合は0を返す
        """
        return  max(self.dic[lab]['min'] - sum([len(l) for l in self.dic[lab]['enrollee']]), 0)

    def able_to_receive(self,lab,is_six):
        """
        研究室labに生徒が入れるかをis_sixに応じてboolで返す
        return -> bool
        """
        if is_six:
            capacity = self.dic[lab]['six_year'] + self.dic[lab]['both']
            buried = sum([len(l) for l in self.dic[lab]['enrollee'][1:]])
        else:
            capacity = self.dic[lab]['four_year'] + self.dic[lab]['both']
            buried = len(self.dic[lab]['enrollee'][0]) + len(self.dic[lab]['enrollee'][2])
        return capacity > buried

    def get_open_labs(self,is_six):
        """
        志望者が6年制かどうかに応じて空き枠の研究室を取得する
        return -> 空き枠のある研究室のidからなる配列
        """
        open_labs = [lab for lab in self.dic if self.able_to_receive(lab,is_six)]
        return open_labs

    def can_exit(self,id):
        """
        idの生徒が他の研究室に移動できる状態かを確認する
        """
        id = self.int_to_str(id)
        lab_id = [d[0] for d in self.dic.items() if search_elem(id,d[1]['enrollee'])]

        # たまに enrolleeに引っかからないことがあるので場合分けした
        if not lab_id:
            print('{}の生徒がLDに見当たりません'.format(id))
            return False
        lab_id = lab_id[0]
        if sum([len(l) for l in self.dic[lab_id]['enrollee']]) > self.dic[lab_id]['min']:
            return True
        else:
            return False

def search_elem(i,box):
    for line in box:
        if i in line:
            return True
    return False
