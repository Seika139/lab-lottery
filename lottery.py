#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
くじ全体の流れ
'''

import numpy as np
import os
import sys

from StudentData import StudentData
from Labdata import LabData


LD = LabData()
SD = StudentData()

def create_data():
    LD.create_dic()
    SD.create_dic()
    load_data()

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
    if SD.dic[id]['state'] == '99':
        return False

    dest_dic = LD.dic[lab]
    four_year = dest_dic['four_year']
    six_year  = dest_dic['six_year']
    both      = dest_dic['both']

    if SD.dic[id]['is_six_course'] == '1':
        if len(dest_dic['enrollee']) < six_year + both:
            LD.move_student(lab,id)
            SD.dic[id]['state'] = '2'
            SD.dic[id]['final_id'] = lab
            return True
        else:
            SD.dic[id]['state'] = '1'
            return False
    else:
        if len(dest_dic['enrollee']) < four_year + both:
            LD.move_student(lab,id)
            SD.dic[id]['state'] = '2'
            SD.dic[id]['final_id'] = lab
            return True
        else:
            SD.dic[id]['state'] = '1'
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
    浪人の抽選以外にも、全体くじで用いる
    input:
        rest_vagabonds = 自分を含めた残りの浪人の数
        id = 浪人のid
    """
    load_data()
    lack_labs = LD.get_lacking_labs()
    lacking_number = sum([i[1] for i in lack_labs])
    print('\n10{}番 : {}さん'.format(int(id)+1,SD.dic[id]['name']))

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
            print('{} -> 「{}」と入力'.format(LD.dic[c]['name'],c))
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

    if lacking_number <= len(vagabonds):
        print('\n浪人の人数が不足枠の数以上あります\n')
    else:
        print('\n浪人の数より不足枠の数が多いです\n')

    while vagabonds:
        id = vagabonds.pop(0)
        move_vagabond(len(vagabonds),id)
    print('浪人の振り分けが終わりました。')

def check_lack_labs():
    lack_labs = LD.get_lacking_labs()

    if not lack_labs:
        print('\n以上で研究室配属プログラムを終了します')
        SD.finalize()
        return []
    else:
        print('\n不足枠が残っているため、全体くじを行います')
        lacking_number = sum([i[1] for i in lack_labs])
        print('全体くじで不足枠に移動する必要があるのは{}人です'.format(lacking_number))

        print('\n不足の研究室は以下の通りです\n')
        for i,l in enumerate(lack_labs):
            print('{} : あと{}人'.format(LD.dic[l[0]]['name'],lack_labs[i][1]))
        print()
        return lack_labs

def vistims_to_one_lab(provisionals,lab,n):
    np.random.shuffle(provisionals)
    lab_name = LD.dic[lab]['name']
    while n > 0:
        if LD.can_move():
            self_movement(lab,provisionals[0])
            print('{} さんは {} に移動です'.format(SD.dic[provisionals[0]['name']],lab_name))
            n -= 1
        del provisionals[0]
    print('\n以上で{}の配属を終わります'.format(lab_name))
    SD.finalize()

def victims_to_several_labs(lack_labs):
    print('不足研究室が複数あるため、アンケートを行います')
    while True:
        n = input('アンケートの取得が完了したら 123 を入力してください\n>> ')
        if n == '123':
            break
        else:
            print()
    dic = edit_form('form_raw.txt')
    max_lab = 0
    min_lab = 100
    for key in dic:
        min_lab = min(min_lab,len(dic[key]))
        max_lab = max(max_lab,len(dic[key]))
    if max_lab / min_lab > 2:
        print('希望の研究室に2倍以上の差があります。全体で統合して抽選を行います')
        provisionals = SD.get_provisionals()
        np.random.shuffle(provisionals)
        for i in range(sum([i[1] for i in lack_labs])):
            move_vagabond(0,provisionals[0])
            del provisionals[0]
    else:
        print('希望の研究室の差は2倍以内です。研究室ごとに抽選を行います')
        for key in dic:
            print('\n' + LD.dic[key]['nane']+'の抽選を行います')
            victims_to_one_lab(dic[key],key,LD.get_lacking_num_by_id(key))

def edit_form(file):
    """
    ファイルの形式が
    lab_id \t student_id
    になっているtxtファイルを辞書にまとめる
    """
    dic = {}
    with open(file,'r') as f:
        form = f.readlines()
    for l in form:
        lab, id = l.split('\t')
        id = int(id.split('\n')[0])
        if lab in dic:
            dic[lab].append(id)
        else:
            dic[lab] = [id]
    return dic

def main():
    create_data()
    first_lottery()
    vagabond_lottery()
    lack_labs = check_lack_labs()
    if len(lack_labs) == 1:
        vistims_to_one_lab(SD.get_provisionals(),lack_labs[0],lack_labs[1])
    elif len(lack_labs) > 1:
        victims_to_several_labs(lack_labs)
    print('以上で配属プログラムを終了します')

if __name__ == '__main__':
    command = sys.argv[1] if len(sys.argv) > 1 else '0'
    if command == '1':
        LD.load_dic()
        i = input('is_six_course ?\n>> ')
        if i == '1':
            ol = LD.get_open_labs('1')
        else:
            ol = LD.get_open_labs('0')
        print(ol)
    else:
        main()
