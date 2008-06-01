import cherrypy
from quickmovie.template import template
from quickmovie.model import meta

from quickmovie.model import Movie

class Main(object):

    @cherrypy.expose
    def plot(self, movie):
        m = meta.Session.query(Movie).filter_by(id = movie)[0]
        return m.plot

    @cherrypy.expose
    def index(self, images = True, plot = False):
        t = {}
        t['movies'] = meta.Session.query(Movie).order_by(Movie.name)
        t['images'] = images
        t['plot'] = plot
        meta.Session.commit()
        return template('index.html', t)
