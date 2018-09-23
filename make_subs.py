from pprint import pprint
import srt
from srt import Subtitle
from datetime import timedelta
import json
import os

filename_subs = 'sub_strings.json'
with open(filename_subs) as f:
    json_obj = json.load(f)
# pprint(json_obj)

filename_filenames = 'filenames.txt'
with open(filename_filenames,'rb') as f:
    filenames = f.readlines()
filenames = [i.strip() for i in filenames]

# print filenames

# 30/33 have subtitles

path = './subs/'
if not os.path.exists(path):
    os.makedirs(path)

def make_subs(filename,sub_data):
    filename = filename.replace('.mov','.srt')
    print filename, sub_data
    subtitles = []

    for item in sorted(sub_data,key=int):
        print item, sub_data[item]

        seconds = int(item)

        index = 1
        start = timedelta(0,seconds,0)
        end = timedelta(0,seconds+10,0)
        content = sub_data[item]

        s = Subtitle(index, start, end, content, proprietary='')

        subtitles.append(s)

    # print srt.compose(subtitles)

    print len(subtitles)

    file = open(path + filename, "wb")
    file.write(srt.compose(subtitles).encode('utf-8'))
    file.close()
    print "output to:",path+filename


count = 0
for item in json_obj:
    # print item
    for str in filenames:
        if item in str:
            count += 1
            # print count, item, str
            filename = str
            sub_data = json_obj[item]
            make_subs(filename, sub_data)
