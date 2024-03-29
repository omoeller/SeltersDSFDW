#!/bin/env python3
# -*- coding: utf-8 -*-

import sys
import re
import os
import random
import datetime

info = sys.argv[1]
txt = sys.argv[2:]

random.seed(4711)

def c2html(c):
    if c in "öäüÖÄÜß&\n<>":
        if c == 'ö':
            return "&ouml;"
        if c == 'ä':
            return "&auml;"
        if c == 'ü':
            return "&uuml;"
        if c == 'Ö':
            return "&Ouml;"
        if c == 'Ä':
            return "&Auml;"
        if c == 'Ü':
            return "&Uuml;"
        if c == 'ß':
            return "&szlig;"
        if c == "&":
            return "&amp;"
        if c == "\n":
            return "<br>"
        if c == "<":
            return "&lt;"
        if c == ">":
            return "&gt;"
    return c

def txt2html(txt):
    return "".join([c2html(x) for x in txt])

def next_col():
    return  random.randint(0, 0xFFFFffff)

pat_ref = re.compile('^([^ =]+)[=]([^,]+)[,].*')

ref = {}
with open(info, 'r') as inf:
    for line in inf:
        m = pat_ref.match(line)
        if m is not None:
            ref[txt2html(m.group(1))] = '<B><FONT COLOR="#{0:08x}">{1}</FONT></B>'.format(next_col(), txt2html(m.group(2)))
keys = list(ref.keys())
            
#sys.stderr.write("USING Mapping: {0}".format(ref))

os.system('git rev-parse HEAD > tmp.TXT')
with open('tmp.TXT', 'r') as inf:
    for line in inf:
        version = line.strip()
os.remove('tmp.TXT')        

print("""<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<HTML>
<HEAD>
<TITLE>Selters - mit den Klons kamen die Tr&auml;nen (Der sch&ouml;nste Film der Welt)</TITLE>
<!-- 
     VERSIONS-STAND: {0}
     DATUM         : {1}
--> </HEAD>
<BODY>
<Ha>Selters - mit den Klons kamen die Tr&auml;nen</H1>
<b>(Der sch&ouml;nste Film der Welt)</b><br>


""".format(version, datetime.datetime.today()))

last = ""
for f in txt:
    print("<H1>{0}</H1>".format(txt2html(f)))
    with open(f, 'r') as inf:
        for line in inf:
            if '#' == line[0]:
                #print("<!-- {0} -->".format(txt2html(line).replace('<br>', '')))
                continue
            line = txt2html(line)
            for k in keys:
                line = line.replace(k, ref[k])
            if (last == "<br>") and (line == "<br>"):
                continue
            print(line)
            last = line
print("""
</BODY>
</HTML>
""")            
          
    

