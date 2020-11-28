from . import main
from flask import render_template,request,redirect,flash
from app import db
from app.models import Movie,DetailUrl,Musicfile,Music,Playlist
from sqlalchemy import or_
import requests


@main.route('/')
def index():
    return render_template('home.html')

@main.route('/movie')
def movie():
    #e rror_out默认为true，请求超出范围返回404错误，如为false则返回空列表
    keyword = request.args.get('keyword')
    if keyword:
        pagination = Movie.query.filter(or_(Movie.name.like('%'+keyword+'%'),Movie.content.like('%' + keyword + '%'))).limit(16).from_self().paginate(1,per_page=16,error_out=False)
        movies = pagination.items
        return render_template('movie/movies.html', movies=movies, pagination=pagination,keyword=keyword)
    page= request.args.get('page',1,type=int)
    pagination = Movie.query.order_by(Movie.timestamp.desc()).paginate(page,per_page=24,error_out=True)
    movies = pagination.items

    return render_template('movie/movies.html',movies=movies,pagination=pagination)

@main.route('/movie/<int:id>')
def get_movie(id):
    movie = Movie.query.get_or_404(id)
    return render_template('movie/movie.html',movie=movie)






@main.route('/music/all')
def music():
    keyword = request.args.get('keyword')
    if keyword:
        pagination = Music.query.filter(
            or_(Music.name.like('%' + keyword + '%'), Music.artist.like('%' + keyword + '%'))).limit(15).from_self().paginate(1, per_page=15,
                                                                                                        error_out=False)
        musics = pagination.items
        length = range(len(musics))
        return render_template('music/all.html', musics=musics, pagination=pagination, keyword=keyword,length=length)
    page = request.args.get('page', 1, type=int)
    pagination = Music.query.paginate(page, per_page=15, error_out=True)
    musics = pagination.items
    length = range(len(musics))

    return render_template('music/all.html', musics=musics, length=length, pagination=pagination)




@main.route('/music/playlists')
def playlists():
    keyword = request.args.get('keyword')
    if keyword:
        pagination = Playlist.query.filter(Playlist.name.like('%' + keyword + '%')).paginate(1, per_page=10,error_out=False)
        playlists = pagination.items
        length = range(len(playlists))
        return render_template('music/playlists.html', playlists=playlists, pagination=pagination, keyword=keyword, length=length)
    page = request.args.get('page', 1, type=int)
    pagination = Playlist.query.paginate(page, per_page=24, error_out=True)
    playlists = pagination.items
    length = range(len(playlists))

    return render_template('music/playlists.html', playlists=playlists, length=length, pagination=pagination)

@main.route('/music/playlist/<int:id>')
def playlist(id):
    playlist = Playlist.query.get_or_404(id)
    musics = playlist.musics
    length = range(len(musics))


    return render_template('music/play_detail.html', playlist=playlist,musics=musics,length=length)


@main.route('/music/<int:rid>')
def songfile(rid):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
    }
    params = {
        'format': 'mp3',
        'rid': rid,
        'response': 'url',
        'type': 'convert_url3',
        'br': '128kmp3',
        'from': 'web',
        't': '1604244829919',
        'httpsStatus': '1',
        'reqId': 'a3b4ce00 - 1c57 - 11eb - 9818 - 998e45cb0736',
    }
    get_download_url = 'http://www.kuwo.cn/url'
    res = requests.get(url=get_download_url, params=params, headers=headers)
    if res.status_code == 200:
        file_url = res.json()['url']
        return redirect(file_url)
    else:
        flash('歌曲资源有误')
        return redirect('main.music')

