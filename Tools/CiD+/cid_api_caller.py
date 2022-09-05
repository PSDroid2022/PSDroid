#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
import re
import ast

out_base = '~/Tools/CiD/OriginCiD31/apicaller'

def caller_extract(line):
    print('line:', line)
    callers = []
    end_pos = line.find(')>')
    while end_pos >= 0:
        caller = line[:end_pos + 2]
        print('caller:', caller)
        callers.append(caller)
        line = line[end_pos + 2:]
        starts = line.find('<')
        line = line[starts:]
        end_pos = line.find(')>')
    return callers

def txt_load(txt_path):
    with open(txt_path) as f:
        lines = [line.strip() for line in f.readlines()]
    idx = 0
    pattern = '^==>Problematic.*?(<.*>):\[.*\]$'
    api_callers = set()
    while idx < len(lines):
        line = lines[idx]
        if line.startswith('==>Problematic'):
            print(line)
            m = re.match(pattern, line)
            if m:
                api = m.group(1)
                idx += 1
                line = lines[idx]
#                callers = ast.literal_eval(str(line))
                callers = caller_extract(line[1:-1])
                for caller in callers:
                    curr = api + '<=' + caller
                    print(curr)
                    api_callers.add(curr)
        idx += 1
    return api_callers

def txt_dump(txt_path, txt_content):
    with open(txt_path, 'w') as f:
        f.write(txt_content)

def txt_traverse():
    txt_base = '~/Tools/CiD/OriginCiD31/CiDAppRunLog'
    txts = os.listdir(txt_base)
    for t in txts:
#        if t.startswith('asdoi#TimeTable.apk'):
#            continue
        t_path = os.path.join(txt_base, t)
        print(t_path)
        if not os.path.exists(t_path):
            continue
        api_caller = txt_load(t_path)
        if api_caller:
            out_path = os.path.join(out_base, t)
            txt_dump(out_path, '\n'.join(list(api_caller)))

if __name__ == '__main__':
    txt_traverse()
