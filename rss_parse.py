from bs4 import BeautifulSoup
import re
import requests
class dmhy_rss(object):
    def __init__(self):
        self.url = 'https://share.dmhy.org/topics/rss/rss.xml'
        self.rule = ''
        self.rss = ''
        self.title = ''
        self.episode = ''
        self.magneturl = ''
    def get_rss(self):
        r = requests.get(self.url, timeout=60)
        self.rss = BeautifulSoup(r.content, 'xml')
    def get_magnet(self):
        title = self.rss.find('title', text=self.rule)
        self.title = title
        magneturl = title.parent.enclosure.attrs['url']
        self.magneturl = magneturl
        return magneturl
    def get_episode(self):
        dmhy_rule = re.compile('[^0-9s]([0-9][0-9])[^0-9bitp月][^bitp月]', re.I)
        results = re.findall(dmhy_rule, self.title.text)
        try:
            self.episode = results[0]
        except IndexError as Argument:
            print('Error in getting episode\n', Argument)
