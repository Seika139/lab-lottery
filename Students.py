#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Students

生徒の情報を管理するクラス
'''


class Student:

    states = {
        0 : '志望者',
        1 : '浪人',
        2 : '仮内定',
        3 : '本内定'
    }

    def __init__(self):
        self.id = 1000                   # 学籍番号
        self.name = None                 # 氏名
        self.destination = None          # 志望先
        self.destination_id = 0          # 志望先のid
        self.is_six_cource = False       # 6年制かどうか
        self.state = Student.states[0]   # 選考状況
        self.lab_id = 0                  # 内定した研究室
