#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
抽選状況をHTMLにまとめる
'''

from StudentData import StudentData
from Labdata import LabData

SD = StudentData()
LD = LabData()

def generate_html():
    SD.load_dic()
    LD.load_dic()
    generate_student_data()
    generate_lab_data()

def generate_student_data():

    with open('html/student_data_temp.html','r',encoding='utf-8') as f:
        lines = f.readlines()
    lines = [i for i in lines]

    def generate_item(id):
        if SD.dic[id]['state'] == '1':
            t =  '<div class="item_red"><div class="name">'
        else:
            t =  '<div class="item"><div class="name">'
        t += '{} : {}'.format(int(id)+1,SD.dic[id]['name'])
        t += '</div><div class="state">'

        if SD.dic[id]['state'] in ['1','7','8']:
            state = SD.states[SD.dic[id]['state']]
        elif SD.dic[id]['state'] == '0':
            state = LD.dic[SD.dic[id]['dest_id']]['name'] + '(志望)'
        elif SD.dic[id]['state'] == '2':
            state = LD.dic[SD.dic[id]['final_id']]['name'] + ' (仮)'
        elif SD.dic[id]['state'] == '3':
            state = LD.dic[SD.dic[id]['final_id']]['name'] + ' (本)'
        else:
            return ''

        t += state + '</div></div>'
        return t

    with open('html/student_data.html','w',encoding='utf-8') as f:
        for i in lines:
            if '{{grid}}' in i:
                i = ''
                for id in SD.dic:
                    i += generate_item(id)
            f.writelines(i)

def generate_lab_data():

    with open('html/lab_data_temp.html','r',encoding='utf-8') as f:
        lines = f.readlines()
    lines = [i for i in lines]

    def genarate_vagabond_head():
        t = '<div class="lab_container_red"><div class="lab_head"><span class="lab_name">'
        t += '浪人'
        t += '</span></div>'
        return t

    def generate_container_top(lab,capacity):
        t =  '<div class="lab_container"><div class="lab_head"><span class="lab_name">'
        t += LD.dic[lab]['name']
        t += '</span><span class="lab_capacity">'
        t += 'min = {}, max = {}'.format(LD.dic[lab]['min'], capacity)
        t += '</span></div>'
        return t

    with open('html/lab_data.html','w',encoding='utf-8') as f:
        for l in lines:
            if '{{container}}' in l:
                l = ''
                vagabonds = SD.get_vagabonds()
                if vagabonds:
                    l += genarate_vagabond_head()
                    l += '<div class="grid">'
                    for id in vagabonds:
                        l += '<div class="names">{}</div>'.format(SD.dic[id]['name'])
                    l += '</div></div>'
                for lab in LD.dic:
                    capacity = LD.dic[lab]['four_year'] + LD.dic[lab]['six_year'] + LD.dic[lab]['both']
                    l += generate_container_top(lab,capacity)
                    l += '<div class="grid">'
                    enrollee = []
                    for i in range(len(LD.dic[lab]['enrollee'])):
                        enrollee.extend(LD.dic[lab]['enrollee'][i])
                    for i in range(capacity):
                        if i < len(enrollee):
                            l += '<div class="names">{}</div>'.format(SD.dic[enrollee[i]]['name'])
                        else:
                            l += '<div class="names"> </div>'
                    l += '</div></div>'
            f.writelines(l)
