from app import db
from manage import app

from app.models import Movie, DetailUrl, Music, Playlist
import re
from jsonpath import jsonpath
import random
import time
import requests
from lxml import etree

def get_vip_music():
    with app.app_context():
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36', }

        session = requests.Session()
        response = session.get('https://www.kuwo.cn/', headers=headers)
        kw_token = dict(response.cookies)
        h = dict(response.headers)

        headers.update({
            'csrf': kw_token['kw_token'],
        })

        url = 'https://www.kuwo.cn/api/www/bang/bang/musicList'
        bangId = [17,145,93,158,16]
        bangId = random.choice(bangId)
        params = {
            'bangId': bangId, #145会员榜  17新歌榜 93飙升榜 158抖音
            'pn': 1,
            'rn': 90,
            'httpsStatus': 1,
        }
        all_song = session.get(url=url, params=params, headers=headers).json()
        all_song = all_song['data']['musicList']
        for song in all_song:
            name = song['name']
            rid = song['rid']
            singer = song['artist']
            length = song['songTimeMinutes']
            album = song['album']
            pic = song['pic']
            # print(name,'获取成功')
            music = Music(name=name,
                          rid=rid,
                          artist=singer,
                          album=album,
                          pic=pic,
                          time_length=length)
            try:
                db.session.add(music)
                db.session.commit()
            except Exception as e:
                print(name, '添加失败')
                # print(e)
                db.session.rollback()

def get_movie():
    with app.app_context():
        for page in range(1, 3):
            url = 'https://www.ygdy8.net/html/gndy/dyzz/list_23_' + str(page) + '.html'

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
            }

            res = requests.get(url=url, headers=headers)
            res.encoding = 'gbk'
            # print(res.text)
            tree = etree.HTML(res.text)
            table_list = tree.xpath('//*[@id="header"]/div/div[3]/div[3]/div[2]/div[2]/div[2]/ul//a')
            for a in table_list:
                url = 'https://www.ygdy8.net' + a.xpath('./@href')[0]
                title = a.xpath('./text()')[0]
                de_url = DetailUrl(url=url, title=title)
                try:
                    db.session.add(de_url)
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    print(e)
                else:
                    res = requests.get(url=url, headers=headers)
                    res.encoding = 'gbk'
                    tree = etree.HTML(res.text)
                    try:
                        name = tree.xpath('/html/body/div[1]/div/div[3]/div[3]/div[1]/div[2]/div[2]/ul//p[1]/text()[1]')[0]
                        name = name.split('\u3000')[-1]
                        # print(name)
                        img_url = tree.xpath('/html/body/div[1]/div/div[3]/div[3]/div[1]/div[2]/div[2]/ul//p/img/@src')[0]
                        # print(img_url)
                        content = tree.xpath('/html/body/div[1]/div/div[3]/div[3]/div[1]/div[2]/div[2]/ul//p//text()')[0:-6]
                        content = '\n'.join(content)
                        down_url = tree.xpath('/html/body/div[1]/div/div[3]/div[3]/div[1]/div[2]/div[2]/ul//p/a/@href')[0]
                        # print(down_url)
                        de_url = DetailUrl.query.filter_by(url=url).first()
                        movie = Movie(url=de_url, content=content, cover=img_url, down_url=down_url, name=name)
                        db.session.add(movie)
                        db.session.commit()
                    except Exception as e:
                        print('重复，下一个')
                        db.session.rollback()
                    else:
                        print(name, '导入成功')
                    time.sleep(1)


def get_playlist():
    with app.app_context():
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36', }

        url = 'https://www.kuwo.cn/api/pc/classify/playlist/getRcmPlayList'
        order = random.choice(['hot','new'])
        params = {
            'pn': 1,
            'rn': 10,
            'order': order,  # new/hot 最新/最热
            'httpsStatus': 1,

        }
        res = requests.get(url=url, headers=headers, params=params)

        if res.status_code == 200:
            page_text = res.json()
            playlist_ids = jsonpath(page_text, '$..id')
            for i in playlist_ids:
                pid = i
                detail_url = 'https://www.kuwo.cn/playlist_detail/' + i
                res = requests.get(url=detail_url, headers=headers)
                if res.status_code == 200:
                    detail_page = res.text
                    tree = etree.HTML(detail_page)
                    title = tree.xpath('//*[@id="__layout"]/div/div[2]/div/div[1]/div[2]/div[1]/p[1]/text()')[0]
                    info = tree.xpath('//*[@id="__layout"]/div/div[2]/div/div[1]/div[1]/p[2]/text()')[0]
                    # print(title, info)
                    slist = tree.xpath('//*[@id="__layout"]/div/div[2]/div/div[1]/div[2]/div[1]/div[2]/div[1]/ul/li')

                    # cover = tree.xpath('//*[@id="__layout"]/div/div[2]/div/div[1]/div[1]/div[1]/img/@src')[0] #无效图片

                    script = re.findall('data:(\[.*?\]),fetch:', detail_page)[0]
                    rids = re.findall(r'rid:(\d+)', script)
                    cover = re.search('img700.*?"(.*?)",', detail_page).group(1).encode('utf-8').decode("unicode_escape")
                    song_num = len(rids)
                    try:
                        playlist = Playlist(
                            name=title,
                            info=info,
                            pid=pid,
                            cover=cover,
                        )
                        # playlist = Playlist.query.filter_by(pid=pid).first()
                        # playlist.cover = cover
                        db.session.add(playlist)
                        db.session.commit()
                        print(title, '歌单添加成功')
                    except Exception as e:
                        # print(e)
                        print(title, '添加失败')
                        db.session.rollback()
                    else:
                        for i in range(song_num):
                            rid = rids[i]
                            name = slist[i].xpath('./div[2]/a/text()')[0]
                            artist = slist[i].xpath('./div[3]//text()')[0]
                            timelength = slist[i].xpath('./div[5]//text()')[0]
                            # print(name, artist, timelength, rid)
                            try:
                                music = Music(
                                    name=name,
                                    artist=artist,
                                    time_length=timelength,
                                    rid=rid,
                                    playlist=Playlist.query.filter_by(pid=pid).first()
                                )
                                db.session.add(music)
                                db.session.commit()
                                print(name, '添加成功')
                            except Exception as e:
                                # print(e)
                                print(name, '添加歌曲失败')
                                db.session.rollback()

                else:
                    print('获取歌单详情页失败')
                time.sleep(3)
        else:
            print('获取歌单列表失败')
