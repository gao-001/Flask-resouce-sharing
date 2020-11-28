from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
from app import login_manage
from app import db


@login_manage.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin,db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64),unique=True,index=True)
    username = db.Column(db.String(60), unique=True)
    password_hash = db.Column(db.String(200))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)

    def __repr__(self):
        return '<User %r>' % self.username



class DetailUrl(db.Model):
    __tablename__ = 'detail_url'
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(200), unique=True)
    title = db.Column(db.String(200), unique=True)
    movie = db.relationship('Movie', backref='url', uselist=False,cascade="all, delete-orphan")

    def __repr__(self):
        return '<Detail %r>' % self.title


class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    detail_id = db.Column(db.Integer, db.ForeignKey('detail_url.id'))
    content = db.Column(db.Text)
    name = db.Column(db.String(100), unique=True)
    cover = db.Column(db.String(255))
    down_url = db.Column(db.Text(500))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Movie %r>' % self.name


class Music(db.Model):
    __tablename__ = 'music'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    artist = db.Column(db.String(100))
    time_length = db.Column(db.String(50))
    rid = db.Column(db.String(100), unique=True)
    album = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    file = db.relationship('Musicfile', backref='music', uselist=False)
    pic = db.Column(db.Text)

    playlist_id=db.Column(db.Integer,db.ForeignKey('playlist.id'))

    def __repr__(self):
        return '<Music %r>' % self.name


class Musicfile(db.Model):
    __tablename__ = 'musicfile'
    id = db.Column(db.Integer, primary_key=True)
    music_id = db.Column(db.Integer, db.ForeignKey('music.id'))
    name = db.Column(db.String(100))
    artist = db.Column(db.String(100))
    url = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Musicfile %r>' % self.name


class Playlist(db.Model):
    __tablename__ = 'playlist'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    pid = db.Column(db.String(100), unique=True)
    info = db.Column(db.Text)
    musics = db.relationship('Music', backref='playlist')
    cover = db.Column(db.Text)

    def __repr__(self):
        return '<Playlist %r>' % self.name

# class Image(db.Model):
#     pass
#
# class Novel(db.Model):
#     pass
#
# class User(db.Model):
#     pass
