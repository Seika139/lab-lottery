#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
くじの流れ
'''

import numpy as np
import os

from StudentData import StudentData
from Labdata import LabData

def first_lottery():

    ld = LabData()
    ld.create_dic()
    ld.load_dic()

    sd = StudentData()
    sd.create_dic()
    sd.load_dic()

    order = [key for key in sd.dic]
    np.random.shuffle(order)
    for id in order:
        if sd.dic[id]['state'] == 99:
            continue

        dest_dic = ld.dic[str(sd.dic[id]['dest_id'])]
        four_year = dest_dic['four_year']
        six_year  = dest_dic['six_year']
        both      = dest_dic['both']

        if sd.dic[id]['is_six_course'] == 1:
            if len(dest_dic['enrollee']) < six_year + both:
                ld.add_student(sd.dic[id]['dest_id'],id)
                sd.dic[id]['state'] = 2
            else:
                sd.dic[id]['state'] = 1
        else:
            if len(dest_dic['enrollee']) < four_year + both:
                ld.add_student(sd.dic[id]['dest_id'],id)
                sd.dic[id]['state'] = 2
            else:
                sd.dic[id]['state'] = 1
    ld.save_dic()
    sd.save_dic()

first_lottery()
