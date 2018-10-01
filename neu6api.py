import re
import requests
import html
import os
from bs4 import BeautifulSoup
from requests_toolbelt.multipart.encoder import MultipartEncoder
import config
FORMHASH = re.compile("<input type=\"hidden\" name=\"formhash\" value=\"(.*?)\"")
FORMHASH2 = re.compile("<input type=\"hidden\" name=\"formhash\" id=\"formhash\" value=\"(.*?)\"")
POSTTIME = re.compile("<input type=\"hidden\" name=\"posttime\" id=\"posttime\" value=\"(.*?)\"")
ATTACHMENT = re.compile("<a href=\"(.*?)\" .*onmouseover=.+\.torrent")
FILENAME = re.compile("\">(.*?)</a>")
class neu6api(object):
    def __init__(self):
        self.base_url = 'http://bt.neu6.edu.cn'
        self.cookies = ''
        self.headers = {
    'upgrade-insecure-requests': "1",
    'user-agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
    'x-devtools-emulate-network-conditions-client-id': "3F7243F966A568624A5829EA9F6B01D4",
    'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    'accept-encoding': "gzip, deflate",
    'accept-language': "zh,en-US;q=0.9,en;q=0.8,ja;q=0.7,zh-TW;q=0.6",
    'cache-control': "no-cache"
    }
    def neu6_login(self, account, password):
        s = requests.Session()
        s.headers.update(self.headers)
        r = s.get(self.base_url, timeout=10)
        LOGINHASH = re.compile("loginhash=(.*?)\"")
        formhash = re.findall(FORMHASH, r.text)[0]
        loginhash = re.findall(LOGINHASH, r.text)[0]
        login_url = 'http://bt.neu6.edu.cn/member.php?mod=logging&action=login&loginsubmit=yes&loginhash=%s&inajax=1' % loginhash
        data = {'formhash': formhash, 'username': account, 'password': password, 'questionid': '0', 'answer': '',
                'cookietime': '2592000'}
        r = s.post(login_url, data=data)
        print(r.text)
        if re.findall("欢迎您回来", r.text):
            self.cookies = s.cookies
            print('neu6 login succeed')
        else:
            print('neu6 login failed')
    def get_config(self):
        self.cookies = config.neu6_getconfig()
    def new_thread(self, fid, typeid, title, content, filename):
        newthread_url = 'http://bt.neu6.edu.cn/forum.php?mod=post&action=newthread&fid='+fid
        r = requests.get(newthread_url, cookies = self.cookies, headers = self.headers, timeout = 10)
        formhash = re.findall(FORMHASH2, r.text)[0]
        posttime = re.findall(POSTTIME, r.text)[0]
        data = {
            'allownoticeauthor': '1',
            'creditlimit': '',
            'formhash': formhash,
            'message': content,
            'mygroupid': '',
            'posttime': posttime,
            'price': '',
            'readperm': '',
            'replylimit': '',
            'rewardfloor': '',
            'rushreplyfrom': '',
            'rushreplyto': '',
            'save': '',
            'mygroupid': '',
            'stopfloor': '',
            'subject': title,
            'tags': '',
            'typeid': typeid,
            'usesig': '1',
            'wysiwyg': '1',
            'special': '127',
            'specialextra': 'torrent',
            'torrent': (os.path.basename(filename), open(filename, 'rb'), 'application/x-bittorrent')
        }
        submit_url = 'http://bt.neu6.edu.cn/forum.php?mod=post&action=newthread&fid='+fid+'&extra=&topicsubmit=yes'
        multipart_data = MultipartEncoder(data)
        tempheaders = self.headers
        tempheaders['content-type'] = multipart_data.content_type
        r = requests.post(submit_url, headers = tempheaders, cookies = self.cookies, data = multipart_data)
        print(r.text)
        print(r.status_code)
        print(r.url)
        return r.url
    def download_torrent_file(self, download_url, directory):
        r = requests.get(download_url, cookies = self.cookies, headers = self.headers, timeout = 10)
        soup = BeautifulSoup(r.text, 'lxml')
        mydivs = soup.findAll("", {"class": "attnm"})
        torrent_info = str(mydivs)
        attachment_url = html.unescape(re.findall(ATTACHMENT, torrent_info)[0])#html entries & = python string &amp;
        filename = re.findall(FILENAME, torrent_info)[0]
        attachment_url = self.base_url + '/' + attachment_url
        r = requests.get(attachment_url, cookies = self.cookies, headers = self.headers, timeout = 10)
        local_filename = directory + '\\' + '[neubt]' + filename
        with open(local_filename, 'wb') as f:
            f.write(r.content)
            # for chunk in r.iter_content(chunk_size=1024):#need stream=True in requests.get
            #     if chunk:  # filter out keep-alive new chunks
            #         f.write(chunk)
            f.flush()
        if os.path.exists(local_filename):
            print('download succeed')
            return local_filename
        else:
            print('download failed')
            return '0'