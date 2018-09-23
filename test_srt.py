from pprint import pprint
import srt
from srt import Subtitle
from datetime import timedelta

subtitle_generator = srt.parse('''\
1
00:31:37,894 --> 00:31:39,928
OK, look, I think I have a plan here.

2
00:31:39,931 --> 00:31:41,931
Using mainly spoons,

3
00:31:41,933 --> 00:31:43,435
we dig a tunnel under the city and release it into the wild.

''')
subtitles = list(subtitle_generator)

# print subtitles[0].start
# datetime.timedelta(0, 1897, 894000)
# print subtitles[1].content
# 'Using mainly spoons,'

# pprint(subtitles)

subtitles = []

# s = Subtitle(index=1,content="text",start=datetime(0,1,0),end=datetime(0,2,0),proprietary='')

index = 1
start = timedelta(0,1,0)
end = timedelta(0,2,0)
content = 'text'

s = Subtitle(index, start, end, content, proprietary='')

print s

print srt.compose([s,s,s,s,s])
