#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
抽選状況をHTMLにまとめる
'''

from StudentData import StudentData
from Labdata import LabData

INPUT = 'html/template.html'
OUTPUT = 'html/generated.html'

SD = StudentData()
LD = LabData()


item_top = '<div class="item"><table><tr><th>番号</th><th>名前</th><th>志望状況</th></tr>'
item_bottom = '</table></div>'
def set_item_middle(id,name,state):
    return '<tr><td class="id">{}</td><td class="name">{}</td><td class="state">{}</td></tr>'.format(id,name,state)

def generate_html():

    SD.load_dic()
    LD.load_dic()

    with open(INPUT,'r',encoding='utf-8') as f:
        lines = f.readlines()
    lines = [i for i in lines]

    with open(OUTPUT,'w',encoding='utf-8') as f:
        for i in lines:
            if '{{grid}}' in i:
                n = 1
                i = ''
                for id in SD.dic:
                    if n == 1:
                        i += item_top
                    name = SD.dic[id]['name']
                    if SD.dic[id]['state'] in ['0','1','7','8']:
                        state = SD.states[SD.dic[id]['state']]
                    elif SD.dic[id]['state'] == '2':
                        state = LD.dic[SD.dic[id]['final_id']]['name'] + ' (仮)'
                    elif SD.dic[id]['state'] == '3':
                        state = LD.dic[SD.dic[id]['final_id']]['name'] + ' (本)'
                    else:
                        n += 1
                        continue
                    name_id = int(id)+1
                    i += set_item_middle(str(name_id),name,state)
                    if n == len(SD.dic):
                        i += item_bottom
                    elif name_id % 10 == 0:
                        i += item_bottom + item_top
                    n += 1
            f.writelines(i)
