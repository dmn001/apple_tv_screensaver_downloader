import re
import codecs
from pprint import pprint
import json

with codecs.open('strings.xml','rb','utf-8') as f:
    data = f.readlines()

data = [i.strip() for i in data]
data = [i.replace(u'\xa0', u' ') for i in data]

print len(data)

output_data = {}

for item in data:
    # print item

    m = re.search('name="(.+?)_(\d+)">(.*)<',item)
    if m:
        # print m.groups()
        # string_for_id[m.group(1)] = m.group(2)

        key = m.group(1)
        seconds = int(m.group(2))
        text = m.group(3)
        # print key, seconds, text

        if key not in output_data:
            output_data[key] = {}
        output_data[key][seconds] = text

pprint(output_data)

file = open('sub_strings.json', "wb")
file.write(json.dumps(output_data,sort_keys=True))
file.close()
