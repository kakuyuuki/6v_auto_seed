import rss_parse
import re
rss = rss_parse.dmhy_rss()
print(rss.url)
rss.rule = re.compile('.*魔卡少女樱.*720p.*', re.I)
rss.get_rss()
magneturl = rss.get_magnet()
rss.get_episode()
print(rss.title)
print(magneturl)
print(rss.episode)