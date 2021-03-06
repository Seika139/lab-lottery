#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
くじ全体の流れ
'''

import codecs
import csv
import json
import numpy as np
import os
import pyperclip
import sys

from StudentData import StudentData
from Labdata import LabData
from generate_html import generate_html


LD = LabData()
SD = StudentData()

def create_data():
    LD.create_dic()
    SD.create_dic()
    generate_html()
    load_data()

def load_data():
    LD.load_dic()
    SD.load_dic()

def save_data():
    LD.save_dic()
    SD.save_dic()
    generate_html()

def move_student(lab,id):
    """
    生徒(id)を研究室(lab)に仮内定させる。
    元々他の研究室にいた場合、そこの仮内定は取り消される。
    return -> bool : 仮内定ができたらTrue
    """
    if SD.dic[id]['state'] in ['7','8','9']:
        return False

    if LD.move_student(lab,id,SD.dic[id]['is_six_course']=='1'):
        SD.dic[id]['state'] = '2'
        SD.dic[id]['final_id'] = lab
        return True
    else:
        SD.dic[id]['state'] = '1'
        return False

def first_lottery():
    """
    最初に行うくじ
    ランダムに選ばれたidの順にmove_student()を行う
    """
    load_data()
    order = [key for key in SD.dic]
    np.random.shuffle(order)
    for id in order:
        move_student(str(SD.dic[id]['dest_id']),id)
    save_data()

def rearrange_and_save():
    """
    enrolleeのfourやsixの枠が空いたときにbothの枠から人を移動する
    """
    for lab in LD.dic:
        students = []
        if len(LD.dic[lab]['enrollee'][2]) > 0:
            for i in range(len(LD.dic[lab]['enrollee'])):
                students.extend(LD.dic[lab]['enrollee'][i])
            for id in students:
                LD.delete_student(id)
                LD.add_student(lab,id,SD.dic[id]['is_six_course']=='1')
            save_data()

def self_movement(lab,id):
    """
    自己申告で研究室に移れる
    return -> bool : 仮内定ができたらTrue
    """
    tf = move_student(lab,id)
    rearrange_and_save()
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
        if lacking_number == 0:
            print('あなたは空き枠に移動してください')
        else:
            print('あなたは空き枠か不足枠に移動してください')
        choice = LD.get_open_labs(SD.dic[id]['is_six_course']=='1')
    else:
        print('あなたは不足枠に移動してください')
        choice = [i[0] for i in lack_labs]

    if len(choice) == 1:
        if self_movement(choice[0],id):
            print('移動すべき研究室は{}のみなので自動的に移動しました。'.format(LD.dic[choice[0]]['name']))
        else:
            print('エラーで移動できません')
    else:
        while True:
            print('以下の研究室の中から選んでください\n')
            print(' '.join(['{} -> {}'.format(c,LD.dic[c]['name']) for c in choice]))
            n = input('>> ')
            if n in choice:
                if self_movement(n,id):
                    print('{}に仮内定しました'.format(LD.dic[n]['name']))
                    break
                else:
                    print('エラーで移動できません')
            else:
                print('選択肢の中にある研究室を入力してください')
    rearrange_and_save()

def vagabond_lottery():
    """
    浪人が空き枠と不足枠を埋めるくじ
    """
    lack_labs = LD.get_lacking_labs()
    lacking_number = sum([i[1] for i in lack_labs])
    vagabonds = SD.get_vagabonds()

    if not vagabonds:
        return None

    np.random.shuffle(vagabonds)

    if lacking_number <= len(vagabonds):
        print('浪人の人数が不足枠の数以上あります')
    else:
        print('浪人の数より不足枠の数が多いです')

    while vagabonds:
        id = vagabonds.pop(0)
        move_vagabond(len(vagabonds)+1,id)
    print('浪人の振り分けが終わりました。')

def absentees_to_lack_lab():
    """
    当日欠席者をランダムに不足枠に振り分ける。
    不足枠より欠席者が多い場合はランダムな空き枠に移動する
    (空き枠がある場合は不足枠が埋まるので全体くじの必要がない)
    """
    absentees = [id for id in SD.dic if SD.dic[id]['state'] == '7']
    if not absentees:
        return None
    np.random.shuffle(absentees)
    lack_labs = []
    for l in LD.get_lacking_labs():
        lack_labs.extend([l[0]]*l[1])
    np.random.shuffle(lack_labs)
    while absentees:
        id = absentees.pop(0)
        if lack_labs:
            lab = lack_labs.pop(0)
            if LD.move_student(lab,id,SD.dic[id]['is_six_course']=='1'):
                SD.dic[id]['state'] = '2'
                SD.dic[id]['final_id'] = lab
        else:
            lab = np.random.shuffle(LD.get_open_labs(SD.dic[id]['is_six_course']=='1'))[0]
            if LD.move_student(lab,id,SD.dic[id]['is_six_course']=='1'):
                SD.dic[id]['state'] = '2'
                SD.dic[id]['final_id'] = lab
    print('欠席者を不足枠にランダムに配置しました')
    save_data()

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

def victims_to_one_lab(provisionals,lab,n):
    """
    provisionals の中から n人 を 研究室 lab に配属させる
    """
    np.random.shuffle(provisionals)
    lab_name = LD.dic[lab]['name']
    while n > 0:
        if LD.can_exit(provisionals[0]):
            self_movement(lab,provisionals[0])
            print('{} さんは {} に移動です'.format(SD.dic[provisionals[0]]['name'],lab_name))
            n -= 1
        del provisionals[0]
    print('\n以上で{}への配属を終わります'.format(lab_name))
    SD.finalize()

def victims_to_several_labs():
    print('不足研究室が複数あるため、アンケートを行います')
    while True:
        n = input('アンケートの取得が完了したら 123 を入力してください\n>> ')
        if n == '123':
            break
    que_dic = csv_to_dic('questionnaire.csv')
    answered_student = []
    for lab in que_dic:
        answered_student.extend(que_dic[lab])
    lack_labs = [i[0] for i in LD.get_lacking_labs()]
    for id in SD.dic:
        if (not id in answered_student) and (not SD.dic[id]['state'] in ['8','9']):
            lab_id = lack_labs[np.random.randint(len(lack_labs))]
            if lab_id in que_dic:
                que_dic[lab_id].append(id)
            else:
                que_dic[lab_id] = [id]
    with codecs.open('json/res_of_questionnaire.json','w',encoding='utf-8') as f:
        dump = json.dumps(que_dic,indent=2,ensure_ascii=False)
        f.write(dump)
    max_lab = 0
    min_lab = 100
    for key in que_dic:
        min_lab = min(min_lab,len(que_dic[key])/LD.get_lacking_num_by_id(key))
        max_lab = max(max_lab,len(que_dic[key])/LD.get_lacking_num_by_id(key))
    if max_lab / min_lab > 2:
        print('希望の研究室に2倍以上の差があります。全体で統合して抽選を行います')
        provisionals = SD.get_provisionals()
        np.random.shuffle(provisionals)
        for i in range(sum([i[1] for i in LD.get_lacking_labs()])):
            move_vagabond(0,provisionals[0])
            del provisionals[0]
        SD.finalize()
    else:
        print('希望の研究室の差は2倍以内です。研究室ごとに抽選を行います')
        for key in que_dic:
            print('\n' + LD.dic[key]['name']+'の抽選を行います')
            victims_to_one_lab(que_dic[key],key,LD.get_lacking_num_by_id(key))

def csv_to_dic(file):
    """
    csvを辞書にまとめる
    """
    with open(file,'r') as f:
        reader = csv.reader(f)
        reader = [i for i in reader]
    dic = {}
    for line in reader:
        if line[0] in dic:
            dic[line[0]].append(line[1])
        else:
            dic[line[0]] = [line[1]]
    return dic

def free_movement():
    """
    first_lotteryの後に自由に動いて良い時間
    """
    while True:
        vagabonds = SD.get_vagabonds()
        if not vagabonds:
            print('浪人がいないので浪人の移動を終わります')
            break
        print('\n現在の浪人は以下の{}人です'.format(len(vagabonds)))
        print('\n'.join(['{} : {}'.format(id,SD.dic[id]['name']) for id in vagabonds]))
        print('\n今なら浪人の人は自由に空き枠・不足枠に移動することができます。')
        print('id の人間が移動する場合は「id」を入力してください')
        id = input('移動のフェーズを終了するなら「qqq」と入力してください。\n>> ')
        if id == 'qqq':
            break
        elif id in vagabonds:
            print('\n{}さんが現在移動できる研究室は以下の通りです'.format(SD.dic[id]['name']))
            choice = LD.get_open_labs(SD.dic[id]['is_six_course']=='1')
            print(' '.join(['{} -> {}'.format(c,LD.dic[c]['name']) for c in choice]))
            print('やっぱり移動しない場合は「q」と入力してください')
            lab = input('>> ')
            if lab in choice:
                if self_movement(lab,id):
                    print('{}に仮内定しました'.format(LD.dic[lab]['name']))
                else:
                    print('エラーで移動できません')
            else:
                print('{}さんは浪人のままです。'.format(SD.dic[id]['name']))
            rearrange_and_save()
        else:
            print('不正な入力です')

def collect_survey():
    """
    アンケートの結果を実際の志望先としてdicに登録する
    """
    SD.load_dic()
    LD.load_dic()
    with open(os.path.join('survey','first_survey.txt')) as f:
        array = f.readlines()
    box = [i.replace('\n','').split('\t') for i in array]
    box = [[int(i[0]),SD.dic[str(int(i[0])-1)]['name'],i[1],LD.get_id_from_name(i[1])] for i in box]
    box.sort()
    box2 = []
    i = 1
    while box:
        if box[0][0] == i:
            box2.append([str(i) for i in box[0]])
            del box[0]
        else:
            box2.append([SD.dic[str(i-1)]['student_num'],SD.dic[str(i-1)]['name'],'なし','999'])
        i += 1
    box2 = [f'{i[0]}\t{i[1]}\t{i[2]}\t{i[3]}' for i in box2]
    copy = '\n'.join(box2)
    pyperclip.copy(copy)

def main(argv):
    if len(argv) > 2:
        print('input a correct args')
    elif len(argv) == 1:
        text = 'input some arguments\n'
        text += '-c : collect_survey\n'
        text += '-e : execute the whole program\n'
        text += '-i : initialize the data'
        print(text)
    else:
        argv = argv[1]
        if argv == '-i':
            print('抽選データを初期化します')
            create_data()
        elif argv == '-c':
            print('第一希望のアンケートを集計します')
            collect_survey()
        elif argv == '-e':
            print('抽選システムを実行します')
            create_data()
            first_lottery()
            free_movement()
            # TODO : 浪人の移動のフェーズの改善
            vagabond_lottery()
            absentees_to_lack_lab()
            # TODO : アンケート結果の取得
            lack_labs = check_lack_labs()
            if len(lack_labs) == 1:
                victims_to_one_lab(SD.get_provisionals(),lack_labs[0][0],lack_labs[0][1])
            elif len(lack_labs) > 1:
                victims_to_several_labs()
            save_data()
            print('以上で配属プログラムを終了します')
        else:
            print('input a correct args')

if __name__ == '__main__':
    main(sys.argv)
