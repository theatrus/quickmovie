import cherrypy
from quickmovie.template import template
from quickmovie.model import meta

from quickmovie.model import Movie

class Main(object):

    @cherrypy.expose
    def index(self):
        t = {}
        t['movies'] = meta.Session.query(Movie).order_by(Movie.name)

        meta.Session.commit()
        return template('index.html', t)
