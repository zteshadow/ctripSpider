#!/bin/bash

echo 'start...' >> /home/samuel_song_bc/spider.txt
export PHANTOMJSPATH=/home/samuel_song_bc/package/phantomjs-1.9.8-linux-x86_64/bin/phantomjs
. /home/samuel_song_bc/.bashrc >> /home/samuel_song_bc/spider.txt
. /home/samuel_song_bc/work/py3env/bin/activate 1>>/home/samuel_song_bc/spider.txt 2>>/home/samuel_song_bc/spider.txt
python3 /home/samuel_song_bc/work/ctripSpider/ctrip.py 1>>/home/samuel_song_bc/spider.txt 2>>/home/samuel_song_bc/spider.txt


