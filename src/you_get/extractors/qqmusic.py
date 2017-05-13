#!/usr/bin/env python

__all__ = ['qqmusic_download']

import os
from json import loads

from ..common import *
from ..common import print_more_compatible as print
from ..util import fs


def qqmusic_hymn():
    return """
    player's Game Over,
    u can abandon.
    u get pissed,
    get pissed,
    Hallelujah my King!
    errr oh! fuck ohhh!!!!
    """


def qqmusic_cloud_music_download(url, output_dir='.', merge=True, info_only=False, **kwargs):
    rid = match1(url, r'album/(.*).html')
    #    if rid is None:
    #        rid = match1(url, r'/(\d+)/?')
    if "album" in url:
        j = loads(get_content("https://musicafe.co/api/get/album/qq?id=%s" % rid,
                              headers={"Referer": "http://music.qq.com/"}))

        artist_name = j['artist']['name'].strip()
        album_name = j['name'].strip()
        new_dir = output_dir + '/' + fs.legitimize("%s - %s" % (artist_name, album_name))
        if not info_only:
            if not os.path.exists(new_dir):
                os.mkdir(new_dir)
            cover_url = j['coverBig']
            download_urls([cover_url], "cover", "jpg", 0, new_dir)

        for i in enumerate(j['songList']):
            song_position = i[0] + 1
            qqmusic_song_download(i[1], output_dir=new_dir, info_only=info_only, song_position=song_position)


def qqmusic_song_download(song, output_dir='.', info_only=False, playlist_prefix="", song_position=""):
    title = "%s%s. %s" % (playlist_prefix, song_position, song['name'])
    url_best = loads(get_content(url="https://musicafe.co/api/get/song/qq?id=003OUlho2HcRHC" % song['id']))
    try:
        qqmusic_download_common(title, url_best,
                                output_dir=output_dir, info_only=info_only)
    except:
        pass


def qqmusic_download_common(title, url_best, output_dir, info_only):
    songtype, ext, size = url_info(url_best)
    print_info(site_info, title, songtype, size)
    if not info_only:
        download_urls([url_best], title, ext, size, output_dir)


def qqmusic_download(url, output_dir='.', merge=True, info_only=False, **kwargs):
    if "music.qq.com" in url:
        qqmusic_cloud_music_download(url, output_dir, merge, info_only, **kwargs)
    else:
        print('This is self_made qqmusic downloader,Error')


site_info = "qq.com"
download = qqmusic_download
download_playlist = playlist_not_supported('qqmusic')
