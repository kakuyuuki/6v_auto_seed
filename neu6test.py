from utorrentapi import UTorrentAPI
apiclient = UTorrentAPI('http://localhost:8080/gui', 'username', 'password')#utorrent webUI username and password
import neu6api
neu6 = neu6api.neu6api()
#neu6.neu6_login('','') # 6v  username and password
#import config
#config.save_cookies(apiclient, neu6)

neu6.get_config()
fid = '44'#anime main
typeid = '222'
title = u'[多田君不恋爱][Tada-kun wa Koi wo Shinai ][01][MP4][SumiSora][发种姬测试标题，如有问题请无视或删除]'.encode('gbk')
content = u'发种姬测试内容，你好吖\n【STORY】'.encode('gbk')
filename = 'E:\\bangumi\others\[SumiSora][Tadakoi][01][GB][720p].mp4.torrent'
download_url,head = neu6.new_thread(fid, typeid, title, content, filename)

#download_url = 'http://bt.neu6.edu.cn/thread-1622837-1-1.html'
directory = 'E:\\bangumi\others'
neu6.download_torrent_file(download_url, directory)
