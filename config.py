import configparser
import os
import json
confile = 'configure.ini'
def check_file():
    config = configparser.ConfigParser()
    if not os.path.exists(confile):
        print('Lack of configure file : configure.ini')
        config['6v'] = {'cookies': ''}
        config['utorrent'] = {'account': '', 'password': '', 'cookies': '', 'token': ''}
        with open(confile, 'w') as configfile:
            config.write(configfile)
        print('new configure file created')
    else:
        print('configure file exists')
def check_data():
    print('did nothing')
def save_cookies(UTorrentAPI,neu6):
    check_file()
    config = configparser.ConfigParser()
    config.read(confile)
    config.set('6v', 'cookies', json.dumps(neu6.cookies.get_dict()).replace('%','%%'))
    config.set('utorrent', 'account', UTorrentAPI.account)
    config.set('utorrent', 'password', UTorrentAPI.password)
    config.set('utorrent', 'cookies', json.dumps(UTorrentAPI.cookies).replace('%','%%'))
    config.set('utorrent', 'token', str(UTorrentAPI.token))
    config.write(open(confile, "w"))
    print('cookies account password saved')
def neu6_getconfig() -> dict:
    check_file()
    config = configparser.ConfigParser()
    config.read(confile)
    cookies = config.get('6v', 'cookies')
    return json.loads(cookies.replace('%%','%'))