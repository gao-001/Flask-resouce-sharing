from app import create_app,db
from app.models import Movie,DetailUrl,Music,Musicfile,Playlist,User
from flask_migrate import Migrate
from flask import render_template
from flask_apscheduler import APScheduler


app = create_app()
migrate = Migrate(app, db)



scheduler = APScheduler(app=app)
scheduler.start()



@app.shell_context_processor
def make_shell_context():
    return dict(db=db,Movie=Movie,DetailUrl=DetailUrl,Music=Music,Musicfile=Musicfile,Playlist=Playlist,User=User)

@app.cli.command()
def deploy():
    from schedule import get_movie,get_playlist,get_vip_music
    db.create_all()
    user = User(username='admin',
                password='admin')
    db.session.add(user)
    db.session.commit()

    get_vip_music()
    get_playlist()
    get_movie()

