from utorrentapi import UTorrentAPI

apiclient = UTorrentAPI('http://localhost:8080/gui', '', '')#utorrent webUI username and password

if apiclient is not None:
    torrents = apiclient.get_list()

    index = 0
    for torrent in torrents['torrents']:
        name = '%i - %s' % (index, torrent[2])
        index+=1
        print(name)
    # apiclient.get_files(torrent[0])
    # apiclient.recheck(torrent[0])
    # apiclient.set_priority(torrent[0], 1, 1)
