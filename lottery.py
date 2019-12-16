#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
くじの流れ
'''

import numpy as np
import os

from StudentData import StudentData
from Labdata import LabData


LD = LabData()
LD.create_dic()
LD.load_dic()

SD = StudentData()
SD.create_dic()
SD.load_dic()

def load_data():
    LD.load_dic()
    SD.load_dic()

def save_data():
    LD.save_dic()
    SD.save_dic()

def move_student(lab,id):
    """
    生徒(id)を研究室(lab)に仮内定させる。
    元々他の研究室にいた場合、そこの仮内定は取り消される。
    return -> bool : 仮内定ができたらTrue
    """
    if SD.dic[id]['state'] == 99:
        return False

    dest_dic = LD.dic[lab]
    four_year = dest_dic['four_year']
    six_year  = dest_dic['six_year']
    both      = dest_dic['both']

    if SD.dic[id]['is_six_course'] == 1:
        if len(dest_dic['enrollee']) < six_year + both:
            LD.move_student(lab,id)
            SD.dic[id]['state'] = 2
            SD.dic[id]['final_id'] = lab
            return True
        else:
            SD.dic[id]['state'] = 1
            return False
    else:
        if len(dest_dic['enrollee']) < four_year + both:
            LD.move_student(lab,id)
            SD.dic[id]['state'] = 2
            SD.dic[id]['final_id'] = lab
            return True
        else:
            SD.dic[id]['state'] = 1
            return False

def first_lottery():
    """
    最初に行うくじ
    ランダムに選ばれたidの順にadd_student()を行う
    """
    load_data()
    order = [key for key in SD.dic]
    np.random.shuffle(order)
    for id in order:
        move_student(str(SD.dic[id]['dest_id']),id)
    save_data()

def self_movement(lab,id):
    """
    自己申告で研究室に移れる
    return -> bool : 仮内定ができたらTrue
    """
    load_data()
    tf = move_student(lab,id)
    save_data()
    return tf

def move_vagabond(rest_vagabonds,id):
    """
    input:
        rest_vagabonds = 自分を含めた残りの浪人の数
        id = 浪人のid
    """
    load_data()
    lack_labs = LD.get_lacking_labs()
    lacking_number = sum([i[1] for i in lack_labs])
    print('\n' + id + ' : ' + SD.dic[id]['name'] + 'さん')

    if lacking_number < rest_vagabonds:
        print('あなたは空き枠か不足枠に移動してください')
        choice = LD.get_open_labs(SD.dic[id]['is_six_course'])
    else:
        print('あなたは不足枠に移動してください')
        choice = [i[0] for i in lack_labs]

    ct = True
    while ct:
        print('以下の研究室の中から選んでください\n')
        for c in choice:
            print(LD.dic[c] + ' : ' + choice)
        n = input('>> ')
        if n in choice:
            if self_movement(n,id):
                print('{}に仮内定しました'.format(LD.dic[n]['name']))
                ct = False
            else:
                print('{}には入れません'.format(LD.dic[n]['name']))
        else:
            print('選択肢の中にある研究室を入力してください')
    save_data()

def vagabond_lottery():
    """
    浪人が空き枠と不足枠を埋めるくじ
    """
    lack_labs = LD.get_lacking_labs()
    lacking_number = sum([i[1] for i in lack_labs])
    vagabonds = SD.get_vagabonds()
    np.random.shuffle(vagabonds)
    print(vagabonds)

    if lacking_number <= rest_vagabonds:
        print('\n浪人の人数が不足枠の数以上あります\n')
    else:
        print('\n浪人の数より不足枠の数が多いです\n')

    while vagabonds:
        rest_vagabonds = len(vagabonds)
        id = vagabonds.pop(0)
        move_vagabond(rest_vagabonds,id)
    print('浪人の振り分けが終わりました。')

first_lottery()
vagabond_lottery()
